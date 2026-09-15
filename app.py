from flask import Flask, jsonify, request
import os
import requests

app = Flask(__name__)

# URL do microsserviço "Calculadora de Nota de Corte" (simulação de FaaS).
# Em Docker Compose, essa variável é injetada apontando para
# http://host.docker.internal:8000/api/CalculaNota (ver docker-compose.yml).
CALCULADORA_URL = os.getenv(
    "CALCULADORA_URL", "http://localhost:8000/api/CalculaNota"
)
@app.route("/")
def home():
 return jsonify({
 "projeto": "Radar ENEM",
 "disciplina": "Computacao em Nuvem",
 "status": "online"
 })
@app.route("/health")
def health():
    return jsonify({"status": "healthy"})
@app.route("/aluno/<nome>")
def aluno(nome):
    ambiente = os.getenv("AMBIENTE", "desenvolvimento")
    return jsonify({
        "aluno": nome,
        "ambiente": ambiente,
        "mensagem": "Bem-vindo ao Mini Radar ENEM"
    })

@app.route("/nota/<int:nota>")
def consultar_nota(nota):
    if nota >= 600:
        classificacao = "acima de 600"
    else:
        classificacao = "abaixo de 600"

    return jsonify({
        "nota": nota,
        "classificacao": classificacao
    })

@app.route("/exibir_nota", methods=["POST"])
def exibir_nota():
    """Consulta o microsserviço externo de cálculo de nota de corte.

    Implementa Resiliência Ativa (Graceful Degradation): o site principal
    (PaaS) nunca fica travado esperando indefinidamente pela API de cálculo
    (FaaS). Se a calculadora estiver lenta ou fora do ar, o usuário recebe
    uma mensagem amigável e o restante do site continua funcionando.
    """
    dados_aluno = request.get_json(silent=True) or {}

    try:
        # O segredo da resiliência: o parâmetro timeout!
        # Se a API demorar mais de 2 segundos para responder, aborta a
        # requisição em vez de travar o site inteiro.
        resposta = requests.post(
            CALCULADORA_URL,
            json={"notas": dados_aluno.get("notas")},
            timeout=2.0,
        )
        resposta.raise_for_status()  # Verifica se a API retornou erro (ex: 500)

        resultado = resposta.json()
        return jsonify(
            {"mensagem": f"Sua nota de corte é: {resultado['nota_corte_calculada']}"}
        )

    except requests.exceptions.Timeout:
        # Graceful Degradation: o serviço demorou demais para responder.
        return jsonify({
            "erro": "A calculadora está com alta demanda neste momento. Continue lendo as notícias."
        }), 503

    except requests.exceptions.ConnectionError:
        # O serviço caiu completamente (ex: terminal da API foi fechado/Ctrl+C).
        return jsonify({
            "erro": "Calculadora temporariamente indisponível. Nossos engenheiros já estão atuando."
        }), 503


if __name__ == "__main__":
 app.run(host="0.0.0.0", port=5000)