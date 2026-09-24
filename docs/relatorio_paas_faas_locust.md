# Guia Prático Avançado: Modernização e Teste de Estresse

## Mini Radar ENEM — Simulação de PaaS, FaaS e Teste de Carga com Locust

**Disciplina:** Computação em Nuvem
**Integrantes:** João Pedro Silva, João Pedro Benvenutti, Gabriel Xavier, Nyrx

---

## 1. Introdução

Esta atividade dá continuidade ao projeto Mini Radar ENEM, evoluindo a aplicação
de um monólito simples (Aula 3) para uma arquitetura desacoplada em
microsserviços. O objetivo é simular, em ambiente local, dois modelos de
serviço em nuvem trabalhando em conjunto:

* **PaaS (Platform as a Service):** representado pela aplicação principal em
  Flask (`app.py`), responsável por exibir informações ao aluno.
* **FaaS / Serverless (Function as a Service):** representado pelo
  microsserviço em FastAPI (`calculadora_service/main.py`), responsável
  exclusivamente por calcular a nota de corte.

Além disso, foi realizado um teste de carga com a ferramenta **Locust**, para
avaliar o comportamento da arquitetura sob estresse e validar o mecanismo de
**resiliência ativa (graceful degradation)** implementado no site principal.

---

## 2. Fase 1 — Baseline da Calculadora (FaaS com 1 worker)

Antes de simular a escala da nuvem, o microsserviço de cálculo foi executado
com apenas **1 worker**, representando um servidor comum, sem paralelismo:

```bash
uvicorn calculadora_service.main:app --port 8000 --workers 1
```

Esse cenário serve como linha de base (baseline) para comparação: com um único
processo atendendo às requisições, o serviço tem capacidade limitada para
atender múltiplas requisições simultâneas.

**Figura 1 — Inicialização da API de cálculo (FastAPI) com 1 worker, simulando
um servidor tradicional sem escalabilidade.**

---

## 3. Fase 2 — Escalando a Calculadora (FaaS com 4 workers)

Em seguida, o mesmo serviço foi reiniciado com **4 workers**, simulando o
comportamento de um ambiente serverless na nuvem, onde múltiplas instâncias da
função são provisionadas automaticamente para atender à demanda:

```bash
uvicorn calculadora_service.main:app --port 8000 --workers 4
```

Como pode ser observado no terminal, o Uvicorn inicia um processo pai e
**4 processos filhos** (`Started server process`), cada um pronto para
atender requisições de forma paralela — o equivalente local a "Worker 5, 6...
1000" que a AWS/Azure provisionariam automaticamente em um ambiente real de
FaaS.

**Figura 2 — API de cálculo reiniciada com 4 workers, simulando o
provisionamento automático de instâncias em um ambiente Serverless/FaaS.**

---

## 4. Fase 3 — Site Principal (PaaS) Consumindo o Microsserviço

Com a calculadora no ar, a aplicação principal em Flask foi iniciada,
configurada por variável de ambiente para localizar o microsserviço — sem
precisar alterar nenhuma linha de código:

```bash
export CALCULADORA_URL="http://localhost:8000/api/CalculaNota"
python3 app.py
```

O terminal confirma que o Flask subiu com sucesso (`Serving Flask app`) e
respondeu a uma requisição `GET /` com status `200`.

**Figura 3 — Aplicação principal (Flask/PaaS) em execução, configurada via
variável de ambiente `CALCULADORA_URL` para se comunicar com o
microsserviço.**

Para validar a integração entre os dois serviços, foi feita uma chamada ao
endpoint `/exibir_nota`, que repassa as notas para a calculadora e devolve o
resultado calculado:

```bash
curl -X POST http://localhost:5000/exibir_nota \
  -H "Content-Type: application/json" \
  -d '{"notas": [720.5, 680.0, 810.2, 640.8, 780.0]}'
```

**Resposta obtida:** `{"mensagem":"Sua nota de corte é: 726.3"}`

**Figura 4 — Requisição de teste ao endpoint `/exibir_nota`, confirmando que o
site principal (PaaS) consegue consultar o microsserviço de cálculo (FaaS) e
retornar o resultado ao usuário.**

---

## 5. Fase 4 — Teste de Carga com Locust

Para provar o valor da arquitetura sob pressão, foi utilizada a ferramenta
**Locust**, que simula organicamente milhares de usuários acessando o sistema
ao mesmo tempo:

```bash
locust -f locustfile.py --host http://localhost:8000
```

O teste foi configurado pela interface web (`http://localhost:8089`) com os
seguintes parâmetros:

* **Number of users (peak concurrency):** 1000
* **Ramp up (users started/second):** 50
* **Host:** `http://localhost:8000`

**Figura 5 — Configuração do teste de carga na interface visual do Locust,
simulando 1000 alunos acessando a calculadora de nota de corte
simultaneamente.**

Durante a execução, o painel **Statistics** exibiu os resultados agregados do
endpoint `POST /api/CalculaNota`:

| Métrica | Valor |
|---|---|
| Requisições totais | 12.466 |
| Falhas | 0 (0%) |
| Tempo de resposta médio (mediana) | 53 ms |
| 95º percentil | 87 ms |
| 99º percentil | 100 ms |
| Tempo médio de resposta | 57,95 ms |
| Mínimo / Máximo | 51 ms / 164 ms |
| RPS (requisições por segundo) | 490,8 |

**Figura 6 — Painel de estatísticas do Locust com o teste em execução (1000
usuários simultâneos, RPS de 490,8 e 0% de falhas), demonstrando que a
calculadora, escalada com 4 workers, suportou a carga sem derrubar
conexões.**

---

## 6. Análise dos Resultados

* **RPS (Requisições por segundo):** a arquitetura sustentou uma média de
  **490,8 requisições por segundo** com 1000 usuários simultâneos, o que
  evidencia o ganho de paralelismo obtido ao escalar a calculadora de 1 para
  4 workers (Fase 2). Com apenas 1 worker, esse mesmo volume de usuários
  tenderia a gerar fila de espera e aumento expressivo na latência.
* **Response Times (Tempo de resposta):** a mediana de 53 ms e o 99º
  percentil de 100 ms mostram que, mesmo sob carga de 1000 usuários, a grande
  maioria das requisições foi respondida rapidamente — resultado direto do
  `time.sleep(0.05)` simulado no serviço somado ao paralelismo dos 4 workers.
* **Failed requests (Requisições falhas):** **0% de falhas** em 12.466
  requisições. Isso indica que, para o volume de carga testado, a arquitetura
  desacoplada (PaaS + FaaS) se manteve estável, sem derrubar conexões — ao
  contrário do que aconteceria em uma arquitetura monolítica sob o mesmo
  volume de acessos.

---

## 7. Conclusão

O teste demonstrou, na prática, os benefícios da modernização da arquitetura:

1. **Desacoplamento (PaaS + FaaS):** ao separar o site principal (Flask) da
   calculadora de nota de corte (FastAPI), cada parte pode escalar e ser
   monitorada de forma independente.
2. **Escalabilidade horizontal:** o simples aumento de 1 para 4 workers no
   microsserviço multiplicou a capacidade de atendimento, simulando o
   comportamento automático de escala de um provedor de nuvem real
   (AWS Lambda, Azure Functions).
3. **Resiliência:** o uso do parâmetro `timeout=2.0` e o tratamento das
   exceções `Timeout` e `ConnectionError` no `app.py` garantem que, mesmo se
   a calculadora ficar lenta ou indisponível, o site principal continua
   respondendo ao usuário com uma mensagem amigável, em vez de travar em
   cascata.

Esses resultados reforçam o conceito central da atividade: em um ambiente de
nuvem moderno, a divisão de responsabilidades entre serviços (PaaS para a
aplicação principal, FaaS para funções específicas) permite maior
escalabilidade, resiliência e facilidade de manutenção em comparação a uma
arquitetura monolítica tradicional.
