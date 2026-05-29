# utils/estados.py

import re


# ── Mapa sigla → nomes aceitos ────────────────────────────────────────────────

ESTADOS = {
    "AC": ["AC", "ACRE"],
    "AL": ["AL", "ALAGOAS"],
    "AP": ["AP", "AMAPÁ", "AMAPA"],
    "AM": ["AM", "AMAZONAS"],
    "BA": ["BA", "BAHIA"],
    "CE": ["CE", "CEARÁ", "CEARA"],
    "DF": ["DF", "DISTRITO FEDERAL"],
    "ES": ["ES", "ESPÍRITO SANTO", "ESPIRITO SANTO"],
    "GO": ["GO", "GOIÁS", "GOIAS"],
    "MA": ["MA", "MARANHÃO", "MARANHAO"],
    "MT": ["MT", "MATO GROSSO"],
    "MS": ["MS", "MATO GROSSO DO SUL"],
    "MG": ["MG", "MINAS GERAIS"],
    "PA": ["PA", "PARÁ", "PARA"],
    "PB": ["PB", "PARAÍBA", "PARAIBA"],
    "PR": ["PR", "PARANÁ", "PARANA"],
    "PE": ["PE", "PERNAMBUCO"],
    "PI": ["PI", "PIAUÍ", "PIAUI"],
    "RJ": ["RJ", "RIO DE JANEIRO"],
    "RN": ["RN", "RIO GRANDE DO NORTE"],
    "RS": ["RS", "RIO GRANDE DO SUL"],
    "RO": ["RO", "RONDÔNIA", "RONDONIA"],
    "RR": ["RR", "RORAIMA"],
    "SC": ["SC", "SANTA CATARINA"],
    "SP": ["SP", "SÃO PAULO", "SAO PAULO"],
    "SE": ["SE", "SERGIPE"],
    "TO": ["TO", "TOCANTINS"],
}

# ── Mapa sigla → nome completo (para exibição) ────────────────────────────────

NOMES_ESTADOS = {
    "AC": "Acre",            "AL": "Alagoas",         "AP": "Amapá",
    "AM": "Amazonas",        "BA": "Bahia",            "CE": "Ceará",
    "DF": "Distrito Federal","ES": "Espírito Santo",   "GO": "Goiás",
    "MA": "Maranhão",        "MT": "Mato Grosso",      "MS": "Mato Grosso do Sul",
    "MG": "Minas Gerais",    "PA": "Pará",             "PB": "Paraíba",
    "PR": "Paraná",          "PE": "Pernambuco",       "PI": "Piauí",
    "RJ": "Rio de Janeiro",  "RN": "Rio Grande do Norte","RS": "Rio Grande do Sul",
    "RO": "Rondônia",        "RR": "Roraima",          "SC": "Santa Catarina",
    "SP": "São Paulo",       "SE": "Sergipe",          "TO": "Tocantins",
}

# ── Regiões para o menu do Telegram ──────────────────────────────────────────

REGIOES = {
    "Norte 🌿": ["AC", "AM", "AP", "PA", "RO", "RR", "TO"],
    "Nordeste ☀️": ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"],
    "Centro-Oeste 🌾": ["DF", "GO", "MS", "MT"],
    "Sudeste 🏙️": ["ES", "MG", "RJ", "SP"],
    "Sul ❄️": ["PR", "RS", "SC"],
}


def detectar_estado(texto: str) -> str | None:
    """
    Detecta a sigla do estado a partir de texto livre.
    Retorna a sigla (ex: 'SP') ou None se não encontrar.
    """
    texto = texto.upper()

    for sigla, nomes in ESTADOS.items():
        for nome in nomes:
            if re.search(rf"\b{re.escape(nome)}\b", texto):
                return sigla

    return None


def nome_estado(uf: str) -> str:
    """Retorna o nome completo do estado pela sigla."""
    return NOMES_ESTADOS.get(uf.upper(), uf)