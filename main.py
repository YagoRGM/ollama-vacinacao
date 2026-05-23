import ollama
from tools import consultar_vacina, horario_posto
from prompts import SYSTEM_PROMPT


def executar_tool(resposta):

    partes = resposta.split(":")

    nome_funcao = partes[1]
    parametro = partes[2]

    if nome_funcao == "consultar_vacina":
        return consultar_vacina(parametro)

    elif nome_funcao == "horario_posto":
        return horario_posto()

    return "Ferramenta não encontrada"


while True:

    pergunta = input("\nVocê: ")

    resposta = ollama.chat(
        model="qwen2.5:1.5b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": pergunta},
        ],
    )

    conteudo = resposta["message"]["content"]

    print("\nModelo:", conteudo)

    if conteudo.startswith("CALL_TOOL"):

        resultado_tool = executar_tool(conteudo)

        resposta_final = ollama.chat(
            model="qwen2.5:1.5b",
            messages=[
                {
                    "role": "system",
                    "content": """
        Você é um assistente de vacinação.

        Responda SOMENTE usando os dados recebidos.
        Não invente informações.
        Seja objetivo e curto.
        """
                },
                {
                    "role": "user",
                    "content": f"""
        Pergunta do usuário:
        {pergunta}

        Resultado:
        {resultado_tool}
        """
                }
            ]
        )

        print("\nAssistente:", resposta_final["message"]["content"])
