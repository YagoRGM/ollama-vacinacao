# tools.py
# Camada de ferramentas: recebe parâmetros brutos do modelo,
# normaliza, chama o database e devolve o resultado.

from database import (
    buscar_cobertura_cidade,
    buscar_cobertura_estado,
    buscar_cobertura_vacina,
    buscar_ranking_estados,
    buscar_vacinas_por_idade,
    buscar_vacinas_por_grupo,
    buscar_efeitos_colaterais,
    buscar_endereco_posto,
    buscar_horario_posto,
)
from utils import normalizar


# ── Cobertura ─────────────────────────────────────────────────────────────────

def consultar_cobertura_cidade(cidade: str) -> str:
    return buscar_cobertura_cidade(normalizar(cidade))


def consultar_cobertura_estado(estado: str) -> str:
    return buscar_cobertura_estado(normalizar(estado))


def consultar_cobertura_vacina(vacina: str) -> str:
    return buscar_cobertura_vacina(normalizar(vacina))


def ranking_estados() -> str:
    linhas = [
        f"{i + 1}. {estado}: {cobertura}"
        for i, (estado, cobertura) in enumerate(buscar_ranking_estados())
    ]
    return "\n".join(linhas)


# ── Recomendações ─────────────────────────────────────────────────────────────

def vacinas_por_idade(idade_str: str) -> list[str]:
    try:
        idade = int(idade_str)
    except ValueError:
        return ["Idade inválida."]
    return buscar_vacinas_por_idade(idade)


def vacinas_por_grupo(grupo: str) -> list[str]:
    return buscar_vacinas_por_grupo(normalizar(grupo))


# ── Informações de Posto ──────────────────────────────────────────────────────

def horario_posto(cidade: str = "") -> str:
    return buscar_horario_posto()


def endereco_posto(cidade: str) -> str:
    return buscar_endereco_posto(normalizar(cidade))


# ── Efeitos Colaterais ────────────────────────────────────────────────────────

def efeitos_colaterais(vacina: str) -> list[str]:
    return buscar_efeitos_colaterais(normalizar(vacina))