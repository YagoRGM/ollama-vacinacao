# tools.py
# Funções Python que executam a lógica real
# A IA apenas decide QUAL chamar e COM QUAL parâmetro

from database import (
    COBERTURA_CIDADES,
    COBERTURA_ESTADOS,
    COBERTURA_VACINAS,
)
from utils import normalizar


def consultar_cobertura_cidade(cidade: str) -> str:
    chave = normalizar(cidade)
    return COBERTURA_CIDADES.get(chave, f"Dados de '{cidade}' não encontrados")


def consultar_cobertura_estado(estado: str) -> str:
    chave = normalizar(estado)
    return COBERTURA_ESTADOS.get(chave, f"Dados de '{estado}' não encontrados")


def ranking_estados() -> str:
    """Retorna todos os estados ordenados por cobertura."""
    ordenados = sorted(
        COBERTURA_ESTADOS.items(),
        key=lambda x: float(x[1].replace("%", "")),
        reverse=True,
    )
    linhas = [f"{i+1}. {estado.title()}: {cob}" for i, (estado, cob) in enumerate(ordenados)]
    return "\n".join(linhas)


def consultar_cobertura_vacina(vacina: str) -> str:
    chave = normalizar(vacina)
    return COBERTURA_VACINAS.get(chave, f"Dados da vacina '{vacina}' não encontrados")


def vacinas_por_idade(idade_str: str) -> list[str]:
    try:
        idade = int(idade_str)
    except ValueError:
        return ["Não entendi a idade. Informe um número, ex: '5' ou '60'."]

    if idade < 1:
        return ["BCG", "Hepatite B"]
    elif idade <= 2:
        return ["BCG", "Hepatite B", "Pentavalente", "Poliomielite", "Rotavírus", "Pneumocócica"]
    elif idade <= 4:
        return ["Tríplice Viral", "Varicela", "DTP Reforço"]
    elif idade <= 9:
        return ["Febre Amarela", "Tríplice Viral Reforço", "Meningocócica C"]
    elif idade <= 14:
        return ["HPV", "Meningocócica ACWY", "dT"]
    elif idade <= 19:
        return ["HPV", "Meningocócica ACWY", "Hepatite B (se não vacinado)"]
    elif idade <= 59:
        return ["Influenza (anual)", "dT a cada 10 anos", "COVID-19"]
    else:
        return ["Influenza (anual)", "COVID-19", "Pneumocócica 23", "Herpes-Zóster"]


def vacinas_por_grupo(grupo: str) -> list[str]:
    chave = normalizar(grupo)

    grupos = {
        "idoso": ["Influenza", "COVID-19", "Pneumocócica 23", "Herpes-Zóster"],
        "idosos": ["Influenza", "COVID-19", "Pneumocócica 23", "Herpes-Zóster"],
        "gestante": ["dTpa", "Hepatite B", "Influenza"],
        "gestantes": ["dTpa", "Hepatite B", "Influenza"],
        "crianca": ["BCG", "Pentavalente", "Poliomielite", "Tríplice Viral", "Febre Amarela"],
        "criancas": ["BCG", "Pentavalente", "Poliomielite", "Tríplice Viral", "Febre Amarela"],
        "adolescente": ["HPV", "Meningocócica ACWY", "dT"],
        "adolescentes": ["HPV", "Meningocócica ACWY", "dT"],
        "adulto": ["Influenza", "dT", "COVID-19", "Hepatite B"],
        "adultos": ["Influenza", "dT", "COVID-19", "Hepatite B"],
        "recem nascido": ["BCG", "Hepatite B"],
        "recem-nascido": ["BCG", "Hepatite B"],
        "recém-nascido": ["BCG", "Hepatite B"],
        "profissional de saude": ["Hepatite B", "Influenza", "Tríplice Viral", "COVID-19"],
        "profissional da saude": ["Hepatite B", "Influenza", "Tríplice Viral", "COVID-19"],
        "indigena": ["Hepatite A", "Hepatite B", "Influenza", "Pneumocócica"],
        "indigenas": ["Hepatite A", "Hepatite B", "Influenza", "Pneumocócica"],
    }

    resultado = grupos.get(chave)
    if resultado:
        return resultado

    return [f"Grupo '{grupo}' não reconhecido. Grupos disponíveis: idosos, gestantes, crianças, adolescentes, adultos, recém-nascidos."]


def horario_posto(cidade: str = "") -> str:
    # No projeto real: consultar API ou banco por cidade
    return "Os postos de saúde (UBS) geralmente funcionam de segunda a sexta, das 7h às 17h. Horários podem variar por município — consulte a prefeitura local."


def endereco_posto(cidade: str) -> str:
    chave = normalizar(cidade)

    postos = {
        "campinas": "UBS Centro — Rua das Flores, 100, Campinas/SP | Tel: (19) 3232-0000",
        "sao paulo": "UBS Paulista — Av. Paulista, 500, São Paulo/SP | Tel: (11) 3333-0000",
        "santos": "UBS Praia — Rua do Porto, 45, Santos/SP | Tel: (13) 3444-0000",
        "rio de janeiro": "UBS Flamengo — Rua das Laranjeiras, 200, Rio de Janeiro/RJ | Tel: (21) 2222-0000",
    }

    resultado = postos.get(chave)
    if resultado:
        return resultado

    return f"Posto não cadastrado para '{cidade}'. No projeto real, isso consultaria a API de UBS do CNES/DATASUS."


def efeitos_colaterais(vacina: str) -> list[str]:
    chave = normalizar(vacina)

    efeitos = {
        "covid": ["dor no local da aplicação", "febre", "cansaço", "dor de cabeça"],
        "covid-19": ["dor no local da aplicação", "febre", "cansaço", "dor de cabeça"],
        "influenza": ["dor no local", "mal-estar leve", "febre baixa"],
        "gripe": ["dor no local", "mal-estar leve", "febre baixa"],
        "hpv": ["dor e vermelhidão no local", "tontura ocasional"],
        "hepatite b": ["dor no local", "cansaço leve"],
        "triplice viral": ["febre, dor de cabeça e manchas vermelhas leves (após 5–12 dias)"],
        "febre amarela": ["dor de cabeça, dores musculares, febre leve (primeiros dias)"],
        "pneumococica": ["vermelhidão no local", "irritabilidade em crianças"],
    }

    resultado = efeitos.get(chave)
    if resultado:
        return resultado

    return [f"Efeitos colaterais de '{vacina}' não cadastrados. Consulte a bula ou um profissional de saúde."]