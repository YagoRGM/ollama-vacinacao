# database.py
# Dados estáticos do sistema de vacinação pública brasileira.
# Todas as funções recebem string normalizada (sem acento, minúscula).

# ── Cobertura por Cidade ──────────────────────────────────────────────────────

_COBERTURA_CIDADE = {
    "campinas":       "88%",
    "sao paulo":      "92%",
    "santos":         "79%",
    "rio de janeiro": "85%",
    "belo horizonte": "83%",
    "curitiba":       "90%",
    "fortaleza":      "77%",
    "salvador":       "75%",
    "recife":         "78%",
    "manaus":         "72%",
}


def buscar_cobertura_cidade(cidade: str) -> str:
    return _COBERTURA_CIDADE.get(cidade, "Cidade não encontrada")


# ── Cobertura por Estado ──────────────────────────────────────────────────────

_COBERTURA_ESTADO = {
    "sao paulo":            "90%",
    "minas gerais":         "87%",
    "rio de janeiro":       "85%",
    "bahia":                "80%",
    "parana":               "89%",
    "santa catarina":       "91%",
    "rio grande do sul":    "88%",
    "pernambuco":           "79%",
    "ceara":                "76%",
    "goias":                "82%",
    "maranhao":             "68%",
    "amazonas":             "71%",
    "para":                 "73%",
    "mato grosso":          "84%",
    "mato grosso do sul":   "86%",
    "sergipe":              "78%",
    "alagoas":              "74%",
    "piaui":                "70%",
    "roraima":              "69%",
    "amapa":                "67%",
    "tocantins":            "75%",
    "rondonia":             "76%",
    "acre":                 "65%",
    "rio grande do norte":  "81%",
    "paraiba":              "77%",
    "espirito santo":       "85%",
    "distrito federal":     "93%",
}


def buscar_cobertura_estado(estado: str) -> str:
    return _COBERTURA_ESTADO.get(estado, "Estado não encontrado")


# ── Cobertura por Vacina ──────────────────────────────────────────────────────

_COBERTURA_VACINA = {
    "covid":          "91%",
    "covid-19":       "91%",
    "influenza":      "84%",
    "gripe":          "84%",
    "hpv":            "76%",
    "hepatite b":     "88%",
    "triplice viral": "85%",
    "sarampo":        "85%",
    "febre amarela":  "79%",
    "meningite":      "82%",
    "tetano":         "86%",
    "poliomielite":   "83%",
    "rotavirus":      "80%",
}


def buscar_cobertura_vacina(vacina: str) -> str:
    return _COBERTURA_VACINA.get(vacina, "Vacina não encontrada")


# ── Ranking de Estados ────────────────────────────────────────────────────────

_RANKING_ESTADOS = [
    ("Distrito Federal",   "93%"),
    ("Santa Catarina",     "91%"),
    ("São Paulo",          "90%"),
    ("Paraná",             "89%"),
    ("Rio Grande do Sul",  "88%"),
    ("Minas Gerais",       "87%"),
    ("Mato Grosso do Sul", "86%"),
    ("Espírito Santo",     "85%"),
    ("Rio de Janeiro",     "85%"),
    ("Mato Grosso",        "84%"),
    ("Goiás",              "82%"),
    ("Rio Grande do Norte","81%"),
    ("Bahia",              "80%"),
    ("Rondônia",           "76%"),
    ("Ceará",              "76%"),
    ("Paraíba",            "77%"),
    ("Sergipe",            "78%"),
    ("Pernambuco",         "79%"),
    ("Piauí",              "70%"),
    ("Tocantins",          "75%"),
    ("Pará",               "73%"),
    ("Alagoas",            "74%"),
    ("Amazonas",           "71%"),
    ("Roraima",            "69%"),
    ("Maranhão",           "68%"),
    ("Amapá",              "67%"),
    ("Acre",               "65%"),
]


def buscar_ranking_estados() -> list[tuple[str, str]]:
    return _RANKING_ESTADOS


# ── Vacinas por Faixa de Idade ────────────────────────────────────────────────

_VACINAS_IDADE = [
    (0,   0,   ["BCG", "Hepatite B"]),
    (1,   5,   ["Poliomielite", "Pentavalente", "Rotavírus"]),
    (6,   17,  ["HPV", "Meningocócica", "dT"]),
    (18,  59,  ["Influenza", "COVID-19", "Hepatite B"]),
    (60,  999, ["Influenza", "COVID-19", "Pneumocócica"]),
]


def buscar_vacinas_por_idade(idade: int) -> list[str]:
    for idade_min, idade_max, vacinas in _VACINAS_IDADE:
        if idade_min <= idade <= idade_max:
            return vacinas
    return ["Faixa etária não encontrada"]


# ── Vacinas por Grupo ─────────────────────────────────────────────────────────

_VACINAS_GRUPO = {
    "idosos":       ["Influenza", "COVID-19", "Pneumocócica"],
    "gestantes":    ["dTpa", "Influenza", "Hepatite B"],
    "criancas":     ["BCG", "Poliomielite", "Tríplice Viral"],
    "adolescentes": ["HPV", "Meningocócica", "dT"],
    "adultos":      ["Influenza", "COVID-19", "dT"],
}


def buscar_vacinas_por_grupo(grupo: str) -> list[str]:
    return _VACINAS_GRUPO.get(grupo, ["Grupo não encontrado"])


# ── Efeitos Colaterais ────────────────────────────────────────────────────────

_EFEITOS_COLATERAIS = {
    "covid":        ["dor no braço", "febre", "cansaço"],
    "covid-19":     ["dor no braço", "febre", "cansaço"],
    "gripe":        ["dor local", "febre leve"],
    "influenza":    ["dor local", "febre leve"],
    "hpv":          ["dor local", "tontura"],
    "bcg":          ["nódulo no local", "cicatriz pequena"],
    "hepatite b":   ["dor no local", "cansaço leve"],
    "febre amarela":["febre leve", "dor de cabeça", "dor muscular"],
    "triplice viral":["febre", "manchas na pele", "dor nas articulações"],
    "poliomielite": ["dor local", "febre leve"],
    "meningite":    ["dor local", "vermelhidão", "febre"],
    "tetano":       ["dor local", "inchaço", "febre leve"],
}


def buscar_efeitos_colaterais(vacina: str) -> list[str]:
    return _EFEITOS_COLATERAIS.get(vacina, ["Efeitos não encontrados"])


# ── Postos de Saúde ───────────────────────────────────────────────────────────

_ENDERECOS_POSTO = {
    "campinas":  "UBS Centro — Rua A, 100",
    "sao paulo": "UBS Paulista — Av. Paulista, 500",
    "santos":    "UBS Praia — Rua do Porto, 45",
    "curitiba":  "UBS Batel — Rua XV de Novembro, 200",
    "recife":    "UBS Boa Viagem — Av. Boa Viagem, 300",
}

_HORARIO_PADRAO = "segunda a sexta, das 7h às 17h"


def buscar_endereco_posto(cidade: str) -> str:
    return _ENDERECOS_POSTO.get(cidade, "Posto não encontrado")


def buscar_horario_posto() -> str:
    return f"Os postos geralmente funcionam de {_HORARIO_PADRAO}."