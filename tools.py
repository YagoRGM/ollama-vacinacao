# tools.py

from database import (
    buscar_cobertura_cidade,
    buscar_cobertura_estado,
    buscar_cobertura_vacina,
    buscar_ranking_estados,
)

from utils import normalizar


# ==========================================
# COBERTURA CIDADE
# ==========================================

def consultar_cobertura_cidade(cidade: str) -> str:

    resultado = buscar_cobertura_cidade(
        normalizar(cidade)
    )

    return resultado


# ==========================================
# COBERTURA ESTADO
# ==========================================

def consultar_cobertura_estado(estado: str) -> str:

    resultado = buscar_cobertura_estado(
        normalizar(estado)
    )

    return resultado


# ==========================================
# COBERTURA VACINA
# ==========================================

def consultar_cobertura_vacina(vacina: str) -> str:

    resultado = buscar_cobertura_vacina(
        normalizar(vacina)
    )

    return resultado


# ==========================================
# RANKING ESTADOS
# ==========================================

def ranking_estados() -> str:

    ranking = buscar_ranking_estados()

    linhas = []

    for i, (estado, cobertura) in enumerate(ranking):

        linhas.append(
            f"{i+1}. {estado}: {cobertura}"
        )

    return "\n".join(linhas)


# ==========================================
# VACINAS POR IDADE
# ==========================================

def vacinas_por_idade(idade_str: str) -> list[str]:

    try:
        idade = int(idade_str)

    except ValueError:

        return [
            "Idade inválida."
        ]

    if idade < 1:

        return [
            "BCG",
            "Hepatite B"
        ]

    elif idade <= 5:

        return [
            "Poliomielite",
            "Pentavalente",
            "Rotavírus"
        ]

    elif idade <= 17:

        return [
            "HPV",
            "Meningocócica",
            "dT"
        ]

    elif idade <= 59:

        return [
            "Influenza",
            "COVID-19",
            "Hepatite B"
        ]

    else:

        return [
            "Influenza",
            "COVID-19",
            "Pneumocócica"
        ]


# ==========================================
# VACINAS POR GRUPO
# ==========================================

def vacinas_por_grupo(grupo: str) -> list[str]:

    grupo = normalizar(grupo)

    grupos = {

        "idosos": [
            "Influenza",
            "COVID-19",
            "Pneumocócica"
        ],

        "gestantes": [
            "dTpa",
            "Influenza",
            "Hepatite B"
        ],

        "criancas": [
            "BCG",
            "Poliomielite",
            "Tríplice Viral"
        ],

        "adultos": [
            "Influenza",
            "COVID-19",
            "dT"
        ],
    }

    return grupos.get(
        grupo,
        ["Grupo não encontrado"]
    )


# ==========================================
# HORÁRIO POSTO
# ==========================================

def horario_posto(cidade: str = "") -> str:

    return (
        "Os postos geralmente funcionam "
        "de segunda a sexta das 7h às 17h."
    )


# ==========================================
# ENDEREÇO POSTO
# ==========================================

def endereco_posto(cidade: str) -> str:

    cidade = normalizar(cidade)

    postos = {

        "campinas":
            "UBS Centro - Rua A, 100",

        "sao paulo":
            "UBS Paulista - Av Paulista, 500",

        "santos":
            "UBS Praia - Rua do Porto, 45",
    }

    return postos.get(
        cidade,
        "Posto não encontrado"
    )


# ==========================================
# EFEITOS COLATERAIS
# ==========================================

def efeitos_colaterais(vacina: str) -> list[str]:

    vacina = normalizar(vacina)

    efeitos = {

        "covid": [
            "dor no braço",
            "febre",
            "cansaço"
        ],

        "gripe": [
            "dor local",
            "febre leve"
        ],

        "hpv": [
            "dor local",
            "tontura"
        ],
    }

    return efeitos.get(
        vacina,
        ["Efeitos não encontrados"]
    )