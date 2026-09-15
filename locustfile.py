"""
Cenário de teste de carga (Fase 3) para simular alunos acessando a
calculadora de nota de corte ao mesmo tempo.

Execução visual (abre navegador em http://localhost:8089):
    locust -f locustfile.py --host http://localhost:8000

Execução headless (linha de comando, gera métricas no terminal):
    locust -f locustfile.py --host http://localhost:8000 \
        --headless -u 200 -r 20 -t 30s --only-summary
"""
from locust import HttpUser, task, between


class AlunoRadarEnem(HttpUser):
    # Simula o tempo de "respiração" de um usuário humano entre requisições.
    wait_time = between(1, 3)

    @task
    def calcular_nota(self):
        payload = {"notas": [720.5, 680.0, 810.2, 640.8, 780.0]}
        self.client.post("/api/CalculaNota", json=payload)
