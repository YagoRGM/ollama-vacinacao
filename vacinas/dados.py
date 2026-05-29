# vacinas/dados.py
# Dados estáticos e funções de busca do módulo de vacinas.
# Nenhuma lógica de Telegram aqui.

from utils.normalizar import normalizar


# ── Vacinas por Faixa de Idade ────────────────────────────────────────────────

_VACINAS_IDADE: list[tuple[int, int, list[str]]] = [
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
    return ["Faixa etária não encontrada."]


# ── Vacinas por Grupo ─────────────────────────────────────────────────────────

_VACINAS_GRUPO: dict[str, list[str]] = {
    "idosos":       ["Influenza", "COVID-19", "Pneumocócica"],
    "gestantes":    ["dTpa", "Influenza", "Hepatite B"],
    "criancas":     ["BCG", "Poliomielite", "Tríplice Viral"],
    "adolescentes": ["HPV", "Meningocócica", "dT"],
    "adultos":      ["Influenza", "COVID-19", "dT"],
    "imunossuprimidos": ["Influenza", "COVID-19", "Pneumocócica", "Herpes-Zóster"],
    "profissionais de saude": ["Influenza", "Hepatite B", "dT", "COVID-19"],
}

# Aliases para facilitar o reconhecimento em texto livre
_ALIASES_GRUPO: dict[str, str] = {
    "idoso":      "idosos",
    "velho":      "idosos",
    "terceira idade": "idosos",
    "gestante":   "gestantes",
    "gravida":    "gestantes",
    "grvida":     "gestantes",
    "grávida":    "gestantes",
    "crianca":    "criancas",
    "criança":    "criancas",
    "bebe":       "criancas",
    "bebê":       "criancas",
    "adolescente":"adolescentes",
    "jovem":      "adolescentes",
    "adulto":     "adultos",
    "imunossuprimido": "imunossuprimidos",
    "profissional de saude": "profissionais de saude",
    "profissional saude": "profissionais de saude",
}


def buscar_vacinas_por_grupo(grupo: str) -> list[str]:
    chave = normalizar(grupo)
    chave = _ALIASES_GRUPO.get(chave, chave)
    return _VACINAS_GRUPO.get(chave, ["Grupo não encontrado."])


def listar_grupos() -> list[str]:
    """Retorna a lista de grupos disponíveis para exibição no menu."""
    return list(_VACINAS_GRUPO.keys())


# ── Efeitos Colaterais ────────────────────────────────────────────────────────

_EFEITOS_COLATERAIS: dict[str, list[str]] = {
    "covid":          ["dor no braço", "febre", "cansaço"],
    "covid-19":       ["dor no braço", "febre", "cansaço"],
    "gripe":          ["dor local", "febre leve"],
    "influenza":      ["dor local", "febre leve"],
    "hpv":            ["dor local", "tontura"],
    "bcg":            ["nódulo no local", "cicatriz pequena"],
    "hepatite b":     ["dor no local", "cansaço leve"],
    "febre amarela":  ["febre leve", "dor de cabeça", "dor muscular"],
    "triplice viral": ["febre", "manchas na pele", "dor nas articulações"],
    "poliomielite":   ["dor local", "febre leve"],
    "meningite":      ["dor local", "vermelhidão", "febre"],
    "tetano":         ["dor local", "inchaço", "febre leve"],
    "dt":             ["dor local", "inchaço", "febre leve"],
    "dtpa":           ["dor local", "inchaço", "febre"],
    "pneumococica":   ["dor local", "febre", "irritabilidade"],
    "rotavirus":      ["irritabilidade", "diarreia leve"],
}


def buscar_efeitos_colaterais(vacina: str) -> list[str]:
    return _EFEITOS_COLATERAIS.get(normalizar(vacina), ["Efeitos não encontrados."])


# ── Informações Gerais por Vacina ─────────────────────────────────────────────

_INFO_VACINAS: dict[str, str] = {
    "bcg": (
        "💉 <b>BCG</b>\n"
        "Protege contra tuberculose grave.\n"
        "Aplicada ao nascimento."
    ),
    "hepatite b": (
        "💉 <b>Hepatite B</b>\n"
        "Protege contra a hepatite B.\n"
        "3 doses: nascimento, 2 e 6 meses."
    ),
    "poliomielite": (
        "💉 <b>Poliomielite (VIP/VOP)</b>\n"
        "Protege contra a poliomielite (paralisia infantil).\n"
        "Doses aos 2, 4, 6 meses e reforços."
    ),
    "hpv": (
        "💉 <b>HPV</b>\n"
        "Protege contra o papilomavírus humano.\n"
        "2 doses para meninas e meninos de 9 a 14 anos."
    ),
    "influenza": (
        "💉 <b>Influenza (Gripe)</b>\n"
        "Protege contra os vírus da gripe.\n"
        "Dose anual. Prioritária para grupos de risco."
    ),
    "covid": (
        "💉 <b>COVID-19</b>\n"
        "Protege contra formas graves da COVID-19.\n"
        "Esquema primário + reforços conforme protocolo."
    ),
    "febre amarela": (
        "💉 <b>Febre Amarela</b>\n"
        "Protege contra a febre amarela.\n"
        "Dose única (dose fracionada em campanhas)."
    ),
}

_ALIASES_VACINA: dict[str, str] = {
    "covid-19":  "covid",
    "coronavirus": "covid",
    "gripe":     "influenza",
    "polio":     "poliomielite",
}


def buscar_info_vacina(vacina: str) -> str | None:
    chave = normalizar(vacina)
    chave = _ALIASES_VACINA.get(chave, chave)
    return _INFO_VACINAS.get(chave)


def listar_vacinas() -> list[str]:
    """Retorna as vacinas disponíveis para info."""
    return list(_INFO_VACINAS.keys())


# ── Formatação de Resultado ───────────────────────────────────────────────────

def formatar_lista_vacinas(titulo: str, vacinas: list[str]) -> str:
    itens = "\n".join(f"  • {v}" for v in vacinas)
    return f"{titulo}\n{itens}"