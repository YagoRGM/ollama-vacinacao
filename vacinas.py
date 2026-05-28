VACINAS = {
    "crianca": [
        "BCG",
        "Hepatite B",
        "Pentavalente",
        "Poliomielite"
    ],

    "adolescente": [
        "HPV",
        "Meningocócica ACWY"
    ],

    "adulto": [
        "Hepatite B",
        "Febre Amarela",
        "dT"
    ],

    "idoso": [
        "Influenza",
        "Covid-19"
    ],

    "gestante": [
        "dTpa",
        "Hepatite B"
    ]
}

def obter_vacinas(grupo):

    return VACINAS.get(
        grupo.lower(),
        []
    )