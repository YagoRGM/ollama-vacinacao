# main.py

# =========================
# BIBLIOTECAS
# =========================

import re
import ollama

from prompts import (
    SYSTEM_PROMPT,
    PROMPT_CLASSIFICADOR
)

from cobertura import (
    buscar_cobertura_estado,
    buscar_cobertura_municipio,
    detectar_municipio,
    obter_estado_do_municipio,
    ranking_estados,
    carregar_dados
)

# =========================
# CONFIGURAÇÕES
# =========================

HISTORICO = []

ESTADOS = [
    "AC", "AL", "AP", "AM", "BA",
    "CE", "DF", "ES", "GO", "MA",
    "MT", "MS", "MG", "PA", "PB",
    "PR", "PE", "PI", "RJ", "RN",
    "RS", "RO", "RR", "SC", "SP",
    "SE", "TO"
]

# =========================
# INICIALIZAÇÃO
# =========================

print("=" * 40)
print("🤖 ASSISTENTE GOTINHA MINI")
print("=" * 40)

print("Carregando dados...")
carregar_dados()
print("Dados carregados.")
print("=" * 40)

# =========================
# HISTÓRICO
# =========================

def adicionar_historico(role, content):

    HISTORICO.append({
        "role": role,
        "content": content
    })

    # mantém pequeno
    if len(HISTORICO) > 10:
        HISTORICO.pop(0)

# =========================
# DETECTAR ESTADO
# =========================

def detectar_estado(texto):

    texto = texto.upper()

    estados = {
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
        "TO": ["TO", "TOCANTINS"]
    }

    for sigla, nomes in estados.items():

        for nome in nomes:

            padrao = rf"\b{re.escape(nome)}\b"

            if re.search(padrao, texto):
                return sigla

    return None

# =========================
# CLASSIFICADOR OLLAMA
# =========================

def classificar(pergunta):

    resposta = ollama.chat(
        model="llama3.2:latest",
        messages=[
            {
                "role": "system",
                "content": PROMPT_CLASSIFICADOR
            },
            {
                "role": "user",
                "content": pergunta
            }
        ]
    )

    return resposta["message"]["content"].strip().upper()

# =========================
# RESPOSTA IA
# =========================

def responder_ia(pergunta):

    resposta = ollama.chat(
        model="llama3.2:latest",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": pergunta
            }
        ]
    )

    return resposta["message"]["content"]

# =========================
# LOOP PRINCIPAL
# =========================

while True:

    pergunta = input("\nVocê: ").strip()

    if not pergunta:
        continue

    pergunta_lower = pergunta.lower()

    adicionar_historico(
        "user",
        pergunta
    )

    # =========================
    # ENCERRAR
    # =========================

    if pergunta_lower in [
        "sair",
        "exit",
        "encerrar",
        "fechar"
    ]:

        print("\n👋 Encerrando...")
        break

    # =========================
    # CLASSIFICAÇÃO
    # =========================

    try:

        classificacao = classificar(pergunta)

    except Exception as e:

        print(f"\n⚠️ Erro no classificador: {e}")
        continue

    print(f"[DEBUG]: {classificacao}")

    # =========================
    # SAUDAÇÃO
    # =========================

    if classificacao == "SAUDACAO":

        resposta = (
            "Olá! 👋\n\n"
            "Sou o Assistente Gotinha 💉\n\n"
            "Posso ajudar com:\n"
            "• Cobertura vacinal\n"
            "• Ranking dos estados\n"
            "• Vacinas\n"
        )

        print(f"\nBot:\n{resposta}")

        adicionar_historico(
            "assistant",
            resposta
        )

        continue

    # =========================
    # RANKING
    # =========================

    if classificacao == "RANKING":

        print("\n🔎 Calculando ranking...\n")

        resposta = ranking_estados()

        print(resposta)

        adicionar_historico(
            "assistant",
            resposta
        )

        continue

    # =========================
    # MUNICÍPIO
    # =========================

    if classificacao == "MUNICIPIO":

        municipio = detectar_municipio(
            pergunta
        )

        if not municipio:

            print(
                "\n⚠️ Município não encontrado."
            )

            continue

        estado = obter_estado_do_municipio(
            municipio
        )

        if not estado:

            print(
                "\n⚠️ Estado não encontrado."
            )

            continue

        print(
            "\n🔎 Buscando cobertura "
            "vacinal do município...\n"
        )

        resposta = buscar_cobertura_municipio(
            estado,
            municipio
        )

        print(resposta)

        adicionar_historico(
            "assistant",
            resposta
        )

        continue

    # =========================
    # COBERTURA POR ESTADO
    # =========================

    if classificacao == "ESTADO_SIGLA":

        estado = detectar_estado(pergunta)

        if not estado:

            print("\n⚠️ Não consegui identificar o estado.")
            continue

        print("\n🔎 Buscando cobertura vacinal...\n")

        resposta = buscar_cobertura_estado(
            estado
        )

        print(resposta)

        adicionar_historico(
            "assistant",
            resposta
        )

        continue

    # =========================
    # COBERTURA
    # =========================

    if classificacao == "COBERTURA":

        resposta = (
            "Digite a sigla do estado.\n\n"
            "Exemplo:\n"
            "• cobertura SP\n"
            "• cobertura RJ"
        )

        print(f"\nBot:\n{resposta}")

        adicionar_historico(
            "assistant",
            resposta
        )

        continue

    # =========================
    # FORA DE CONTEXTO
    # =========================

    if classificacao == "FORA_CONTEXTO":

        resposta = (
            "Sou o Assistente Gotinha 💉\n\n"
            "Posso ajudar apenas com:\n"
            "• vacinação\n"
            "• cobertura vacinal\n"
            "• imunização\n"
            "• SUS"
        )

        print(f"\nBot:\n{resposta}")

        adicionar_historico(
            "assistant",
            resposta
        )

        continue

    # =========================
    # FALLBACK IA
    # =========================

    try:

        resposta = responder_ia(
            pergunta
        )

        print(f"\nBot:\n{resposta}")

        adicionar_historico(
            "assistant",
            resposta
        )

    except Exception as e:

        print(f"\n⚠️ Erro: {e}")