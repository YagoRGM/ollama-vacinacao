# database.py
# No projeto real, esses dados vêm de scraping + Excel/CSV do DATASUS
# Aqui são fictícios para o laboratório

COBERTURA_CIDADES = {
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

COBERTURA_ESTADOS = {
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

COBERTURA_VACINAS = {
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