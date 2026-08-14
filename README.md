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