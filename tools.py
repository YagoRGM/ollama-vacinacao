def consultar_vacina(cidade):
    dados = {
        "são paulo": "Cobertura vacinal: 92%",
        "campinas": "Cobertura vacinal: 88%",
        "santos": "Cobertura vacinal: 79%"
    }

    return dados.get(cidade.lower(), "Cidade não encontrada")


def horario_posto():
    return "Os postos funcionam das 8h às 17h"