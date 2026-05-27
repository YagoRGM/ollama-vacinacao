# database.py

# ==========================================
# COBERTURA POR CIDADE
# ==========================================

def buscar_cobertura_cidade(cidade):

    dados = {
        "campinas": "88%",
        "sao paulo": "92%",
        "santos": "79%",
        "rio de janeiro": "85%",
        "belo horizonte": "83%",
        "curitiba": "90%",
        "fortaleza": "77%",
        "salvador": "75%",
        "recife": "78%",
        "manaus": "72%",
    }

    return dados.get(
        cidade.lower(),
        "Cidade não encontrada"
    )


# ==========================================
# COBERTURA POR ESTADO
# ==========================================

def buscar_cobertura_estado(estado):

    dados = {
        "sao paulo": "90%",
        "minas gerais": "87%",
        "rio de janeiro": "85%",
        "bahia": "80%",
        "parana": "89%",
        "santa catarina": "91%",
        "rio grande do sul": "88%",
        "pernambuco": "79%",
        "ceara": "76%",
        "goias": "82%",
        "maranhao": "68%",
        "amazonas": "71%",
        "para": "73%",
        "mato grosso": "84%",
        "mato grosso do sul": "86%",
        "sergipe": "78%",
        "alagoas": "74%",
        "piaui": "70%",
        "roraima": "69%",
        "amapa": "67%",
        "tocantins": "75%",
        "rondonia": "76%",
        "acre": "65%",
        "rio grande do norte": "81%",
        "paraiba": "77%",
        "espirito santo": "85%",
        "distrito federal": "93%",
    }

    return dados.get(
        estado.lower(),
        "Estado não encontrado"
    )


# ==========================================
# COBERTURA POR VACINA
# ==========================================

def buscar_cobertura_vacina(vacina):

    dados = {
        "covid": "91%",
        "covid-19": "91%",
        "influenza": "84%",
        "gripe": "84%",
        "hpv": "76%",
        "hepatite b": "88%",
        "triplice viral": "85%",
        "sarampo": "85%",
        "febre amarela": "79%",
        "meningite": "82%",
        "tetano": "86%",
        "poliomielite": "83%",
        "rotavirus": "80%",
    }

    return dados.get(
        vacina.lower(),
        "Vacina não encontrada"
    )


# ==========================================
# RANKING ESTADOS
# ==========================================

def buscar_ranking_estados():

    ranking = [
        ("Distrito Federal", "93%"),
        ("São Paulo", "90%"),
        ("Santa Catarina", "91%"),
        ("Paraná", "89%"),
        ("Rio Grande do Sul", "88%"),
        ("Minas Gerais", "87%"),
        ("Acre", "65%"),
        ("Amapá", "67%"),
        ("Maranhão", "68%"),
    ]

    return ranking