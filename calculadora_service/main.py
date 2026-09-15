"""
Microsserviço "Calculadora de Nota de Corte" (simulação de FaaS / Serverless).

Este serviço é isolado do site principal (app.py / Flask) para representar
o desacoplamento de arquitetura de monólito -> microsserviços, conforme
descrito na Fase 2 do guia da atividade.

Executar localmente (Baseline - 1 worker):
    uvicorn calculadora_service.main:app --port 8000 --workers 1

Executar simulando escala de nuvem (4 workers):
    uvicorn calculadora_service.main:app --port 8000 --workers 4
"""
import time
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, Field


class Notas(BaseModel):
    """Validação de dados de entrada via Pydantic.

    Garante que o payload recebido seja sempre uma lista de números
    decimais. Qualquer formato inválido (texto, lista vazia, etc.) é
    rejeitado automaticamente pelo FastAPI com HTTP 422.
    """
    notas: List[float] = Field(..., min_length=1, description="Lista de notas do aluno")


app = FastAPI(title="Calculadora de Nota de Corte - Radar ENEM")


@app.get("/")
def root():
    return {
        "servico": "Calculadora de Nota de Corte",
        "modelo_simulado": "FaaS / Serverless",
        "status": "online",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/api/CalculaNota")
def calcular(payload: Notas):
    # Simulação de processamento pesado (equivalente ao cálculo real da
    # Teoria de Resposta ao Item - TRI). Sem esse atraso artificial, o
    # cálculo de média simples seria rápido demais para evidenciar o
    # comportamento do sistema sob teste de carga.
    time.sleep(0.05)

    nota_corte = sum(payload.notas) / len(payload.notas)
    return {"nota_corte_calculada": round(nota_corte, 2)}
