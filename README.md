# Mini Radar ENEM com-Python-e-Docker-Aula-3-Modelos-de-servico-IaaS-PaaS-SaaS

## 📌 Sobre o Projeto
Este repositório contém a entrega da Atividade Prática da Aula 3 de Computação em Nuvem[cite: 1]. O objetivo do projeto é executar uma pequena API Python localmente, empacotá-la em um container Docker e analisar as responsabilidades envolvidas nos diferentes modelos de serviço em nuvem (IaaS, PaaS, SaaS)[cite: 1].

## 🛠 Tecnologias Utilizadas
* Python 3[cite: 1]
* Flask[cite: 1]
* Docker (Dockerfile e containers)[cite: 1]

## 📋 Pré-requisitos
Para rodar este projeto, você precisará ter instalado em sua máquina:
* Python 3[cite: 1]
* Docker Desktop ou Docker Engine funcionando[cite: 1]
* Editor de código ou IDE[cite: 1]
* Terminal ou PowerShell[cite: 1]

## 🚀 Como executar a aplicação

### 1. Sem Docker (Ambiente Virtual)
1. Crie o ambiente virtual com o comando `python -m venv venv`[cite: 1]
2. Ative o ambiente virtual (`source venv/bin/activate` no Linux/macOS ou `venv\Scripts\Activate.ps1` no Windows)[cite: 1]
3. Instale as dependências executando `pip install -r requirements.txt`[cite: 1]
4. Inicie o servidor com `python app.py`[cite: 1]
5. Acesse no navegador: `http://localhost:5000`[cite: 1]

### 2. Com Docker
1. Construa a imagem Docker com o comando: `docker build -t radar-enem:v1 .`[cite: 1]
2. Execute o container mapeando a porta 5000: `docker run --rm -p 5000:5000 radar-enem:v1`[cite: 1]
3. Para rodar a versão atualizada (v2) com o endpoint de notas, faça o build da versão 2: `docker build -t radar-enem:v2 .` e rode da mesma forma alterando a tag para `v2`[cite: 1].

**Dica:** É possível injetar variáveis de ambiente no container para alterar o contexto (ex: produção vs desenvolvimento) usando a flag `-e`:
`docker run --rm -p 5000:5000 -e AMBIENTE=producao radar-enem:v1`[cite: 1]

## 🌐 Endpoints Disponíveis
A API possui as seguintes rotas:
* `/`: Retorna as informações principais do projeto e da disciplina (Computação em Nuvem)[cite: 1]
* `/health`: Rota de verificação para saber se o serviço está saudável (`"status": "healthy"`)[cite: 1]
* `/aluno/<nome>`: Retorna uma mensagem de boas-vindas com o nome do aluno e exibe o ambiente configurado na variável de ambiente[cite: 1]
* `/nota/<int:nota>`: Endpoint da versão 2 (v2) que recebe uma nota e retorna uma classificação indicando se ela está "acima de 600" ou "abaixo de 600"[cite: 1]

## 📝 Entregáveis
De acordo com os requisitos da atividade, este repositório contém:
* Os arquivos `app.py` e `requirements.txt`[cite: 1]
* O arquivo `Dockerfile` responsável por gerar a imagem[cite: 1]
* Evidências do container em execução (ver diretório correspondente)[cite: 1]
* O arquivo `docs/aula03.md` contendo as respostas conceituais e análises sobre IaaS e PaaS[cite: 1]

---

## 🚀 Guia Prático Avançado: Modernização e Teste de Estresse

Esta segunda parte do projeto evolui a aplicação de um monólito simples para uma arquitetura
desacoplada, simulando **PaaS** (site principal) e **FaaS/Serverless** (microsserviço de cálculo),
além de um teste de carga com **Locust**.

### Arquitetura

* `app.py` — Site principal (Flask), simula o **PaaS**. Expõe o endpoint `POST /exibir_nota`.
* `calculadora_service/main.py` — Microsserviço de cálculo de nota de corte (FastAPI), simula o
  **FaaS/Serverless**. Expõe o endpoint `POST /api/CalculaNota`.
* `locustfile.py` — Cenário de teste de carga (`AlunoRadarEnem`) que ataca o microsserviço.
* `docker-compose.yml` — Orquestra `web_app` + `locust_tester` numa rede virtual (`radar_network`),
  simulando o ecossistema de nuvem localmente.

### Fase 1 — Rodando com Docker Compose (PaaS + Locust visual)

```powershell
docker compose up --build
```

* Site principal: http://localhost:5000
* Locust (interface web): http://localhost:8089

> Nota: como não há uma imagem publicada em `seudockerhub/radar-enem`, o `docker-compose.yml`
> faz o **build local** a partir do `Dockerfile` deste repositório (`build: context: .`).
> O serviço `web_app` sozinho não sobe a calculadora — rode-a separadamente (Fase 2) ou
> adicione um serviço equivalente ao compose caso queira tudo em containers.

### Fase 2 — Calculadora de Nota (FastAPI / FaaS)

1. Instale as dependências do microsserviço:
   ```powershell
   pip install -r calculadora_service/requirements.txt
   ```
2. Baseline (1 worker) — evidencia o gargalo de um servidor comum:
   ```powershell
   uvicorn calculadora_service.main:app --port 8000 --workers 1
   ```
3. Simulando escala de nuvem (4 workers):
   ```powershell
   uvicorn calculadora_service.main:app --port 8000 --workers 4
   ```

### Fase 3 — Site principal consumindo o microsserviço

Em outro terminal, com a calculadora já rodando:

```powershell
$env:CALCULADORA_URL = "http://localhost:8000/api/CalculaNota"
python app.py
```

Teste manualmente:

```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:5000/exibir_nota `
  -ContentType "application/json" `
  -Body '{"notas": [720.5, 680.0, 810.2, 640.8, 780.0]}'
```

### Fase 4 — Teste de Carga com Locust

Interface visual (abra `http://localhost:8089` no navegador):

```powershell
locust -f locustfile.py --host http://localhost:8000
```

Modo headless (linha de comando, direto no terminal, sem navegador):

```powershell
locust -f locustfile.py --host http://localhost:8000 --headless -u 200 -r 20 -t 30s --only-summary
```

Métricas a observar (aba **Charts** no modo visual, ou resumo final no modo headless):

1. **Failed requests** — requisições que falharam (arquitetura não aguentou o tranco).
2. **RPS (Requisições por segundo)** — velocidade da arquitetura. Compare 1 worker x 4 workers.
3. **Response Times** — tempo médio de espera do "aluno" pela nota.

### Fase 5 — Resiliência Ativa (Graceful Degradation)

O endpoint `/exibir_nota` do `app.py` usa `timeout=2.0` nas chamadas ao microsserviço e trata
`Timeout` e `ConnectionError` retornando HTTP 503 com mensagens amigáveis, em vez de deixar o
site principal travar em cascata:

* Se a calculadora estiver lenta (sob ataque do Locust): *"A calculadora está com alta demanda
  neste momento. Continue lendo as notícias."*
* Se a calculadora estiver fora do ar (ex: `Ctrl+C` no terminal do FastAPI): *"Calculadora
  temporariamente indisponível. Nossos engenheiros já estão atuando."*

Para reproduzir: inicie um ataque no Locust, acesse `/exibir_nota` enquanto a latência sobe, depois
derrube o FastAPI (`Ctrl+C`) e acesse novamente — o site principal continua respondendo.