import ollama

from prompts import SYSTEM_PROMPT, RETRY_PROMPT
from utils import (
    parse_resposta_modelo,
    log_modelo,
    pergunta_e_sobre_vacina,
    pergunta_quer_dados,
    resposta_parece_alucinacao,
    historico_sanitizado,
    pergunta_e_saudacao,
)
from tools import (
    consultar_cobertura_cidade,
    consultar_cobertura_estado,
    consultar_cobertura_vacina,
    ranking_estados,
    vacinas_por_idade,
    vacinas_por_grupo,
    horario_posto,
    endereco_posto,
    efeitos_colaterais,
)

# ── Configuração ─────────────────────────────────────────────────────────────
MODEL = "qwen2.5:3b"
DEBUG = True
MAX_RETRIES = 2
# ─────────────────────────────────────────────────────────────────────────────

ROUTER = {
    "consultar_cobertura_cidade": consultar_cobertura_cidade,
    "consultar_cobertura_estado": consultar_cobertura_estado,
    "consultar_cobertura_vacina": consultar_cobertura_vacina,
    "ranking_estados":            ranking_estados,
    "vacinas_por_idade":          vacinas_por_idade,
    "vacinas_por_grupo":          vacinas_por_grupo,
    "horario_posto":              horario_posto,
    "endereco_posto":             endereco_posto,
    "efeitos_colaterais":         efeitos_colaterais,
}

MSG_FORA_TEMA = (
    "Sou especializado em vacinação pública brasileira e não posso ajudar com outros assuntos. "
    "Posso informar sobre coberturas vacinais, vacinas por idade ou grupo, postos de saúde e muito mais!"
)
MSG_SEM_DADOS = (
    "Não consegui localizar essa informação. "
    "Tente perguntar sobre uma cidade, estado ou vacina específica."
)

# Palavras que indicam follow-up de vacinação em perguntas do USUÁRIO
# Ex: "e do rio?" após cobertura, "e para idosos?" após grupo
# Só lemos mensagens do usuário, nunca do assistente, para evitar contaminação
_FOLLOWUP_VACINA = [
    "cobertura", "vacina", "imuniza", "posto", "ubs", "efeito",
    "colateral", "dose", "grupo", "idade", "ranking", "estado",
    "cidade", "gripe", "covid", "hpv", "bcg", "hepatite", "influenza",
    "gestante", "idoso", "crianca", "adolescente", "adulto",
]


def _tem_contexto_vacina_no_historico(historico: list[dict], janela: int = 4) -> bool:
    """
    Verifica se alguma das últimas `janela` mensagens DO USUÁRIO
    continha palavras de vacinação. Isso indica que uma pergunta curta
    como 'e do rio?' é um follow-up legítimo.

    IMPORTANTE: lemos só role=user — nunca role=assistant.
    A MSG_FORA_TEMA do assistente contém palavras como "coberturas vacinais"
    e "postos de saúde", o que contaminava o filtro de contexto.
    """
    msgs_usuario = [
        m for m in historico if m["role"] == "user"
    ][-janela:]

    for msg in msgs_usuario:
        texto = msg["content"].lower()
        if any(kw in texto for kw in _FOLLOWUP_VACINA):
            return True
    return False


def executar_tool(tool: str, parametro: str):
    func = ROUTER.get(tool)
    if func is None:
        return None, f"Ferramenta '{tool}' não reconhecida."
    try:
        if parametro == "none":
            parametro = ""
        resultado = func(parametro) if parametro else func()

        return resultado, None
    except Exception as e:
        return None, f"Erro ao executar '{tool}': {e}"


def montar_resposta(tool: str, parametro: str, resultado) -> str:
    if isinstance(resultado, list):
        itens = "\n".join(f"  • {item}" for item in resultado)
        resultado_str = f"\n{itens}"
    else:
        resultado_str = str(resultado)

    param_label = parametro

    if param_label:
        param_label = param_label.title()

    templates = {
        "consultar_cobertura_cidade": f"A cobertura vacinal de {param_label} é {resultado_str}.",
        "consultar_cobertura_estado": f"A cobertura vacinal do estado {param_label} é {resultado_str}.",
        "consultar_cobertura_vacina": f"A cobertura da vacina {param_label} é {resultado_str}.",
        "ranking_estados":            f"Ranking de cobertura vacinal por estado:\n{resultado_str}",
        "vacinas_por_idade":          f"Vacinas recomendadas para {parametro} anos:{resultado_str}",
        "vacinas_por_grupo":          f"Vacinas recomendadas para {parametro.lower() if parametro else ''}:{resultado_str}",
        "horario_posto":              resultado_str,
        "endereco_posto":             f"Informações do posto em {param_label}:\n  {resultado_str}",
        "efeitos_colaterais":         f"Efeitos colaterais comuns da vacina {param_label}:{resultado_str}",
    }
    return templates.get(tool, resultado_str)


def chat_com_modelo(historico: list[dict]) -> str:

    resposta = ollama.chat(

        model=MODEL,

        messages=historico,

        options={

            "temperature": 0,

            "top_p": 0.1,

            "num_predict": 120,
        }
    )

    return resposta["message"]["content"].strip()


def processar_turno(pergunta: str, historico: list[dict]) -> tuple[str, str, bool, bool]:
    """
    Retorna: (resposta_final, resposta_raw, deve_salvar_no_historico)

    O terceiro valor indica se a resposta deve entrar no histórico.
    Respostas de fora do tema NÃO entram — evita contaminar o contexto do modelo.
    """

    # ── Saudação ─────────────────────────────────────

    if pergunta_e_saudacao(pergunta):

        return (
            "Olá! Posso ajudar com informações sobre vacinação, postos de saúde e vacinas.",
            "[saudacao]",
            False,
            False,
        )

    # ── Passo 1: filtro de tema ───────────────────────────────────────────────
    # Follow-ups curtos ("e do rio?", "e para idosos?") passam se o usuário
    # falou de vacinação nas últimas 4 mensagens.
    # NUNCA usamos mensagens do assistente para esse check.
    e_sobre_vacina = pergunta_e_sobre_vacina(pergunta)
    tem_followup = _tem_contexto_vacina_no_historico(historico)

    if not e_sobre_vacina and not tem_followup:
        if DEBUG:
            print(f"\n[FILTRO] Fora do tema — bloqueada por Python.")
        # False = não salvar no histórico (pergunta e resposta descartadas)
        return MSG_FORA_TEMA, "[bloqueado por filtro de tema]", False, False

    # ── Passo 2: consulta ao modelo ───────────────────────────────────────────
    historico_limpo = historico_sanitizado(historico)
    resposta_raw = chat_com_modelo(historico_limpo)

    if DEBUG:
        print(f"\n[DEBUG modelo raw]: {resposta_raw}")

    parsed = parse_resposta_modelo(resposta_raw)

    if DEBUG:
        print(f"[PARSED]: {parsed}")

    if parsed["tipo"] == "tool":
        resultado, erro = executar_tool(parsed["tool"], parsed["parametro"])
        if erro:
            return erro, resposta_raw, True
        return montar_resposta(parsed["tool"], parsed["parametro"], resultado), resposta_raw, True, False

    # ── Passo 3: modelo respondeu livre — verificar se deveria chamar tool ────
    texto_livre = parsed["texto"]
    deveria_chamar_tool = pergunta_quer_dados(pergunta) or resposta_parece_alucinacao(texto_livre)

    if not deveria_chamar_tool:
        return texto_livre, resposta_raw, True, False

    # ── Passo 4: retry ────────────────────────────────────────────────────────
    for tentativa in range(1, MAX_RETRIES + 1):
        if DEBUG:
            print(f"\n[RETRY {tentativa}/{MAX_RETRIES}] Forçando CALL_TOOL...")

        historico_retry = historico_limpo + [
            {"role": "assistant", "content": texto_livre},
            {"role": "user", "content": RETRY_PROMPT.format(pergunta=pergunta)},
        ]

        resposta_raw = chat_com_modelo(historico_retry)

        if DEBUG:
            print(f"[DEBUG retry raw]: {resposta_raw}")

        parsed_retry = parse_resposta_modelo(resposta_raw)

        if parsed_retry["tipo"] == "tool":
            resultado, erro = executar_tool(parsed_retry["tool"], parsed_retry["parametro"])
            if erro:
                return erro, resposta_raw, True
            return montar_resposta(parsed_retry["tool"], parsed_retry["parametro"], resultado), resposta_raw, True

        texto_livre = parsed_retry["texto"]

    if DEBUG:
        print(f"[AVISO] {MAX_RETRIES} retries esgotados.")

    return MSG_SEM_DADOS, resposta_raw, True


def main():
    print(f"\n{'═' * 55}")
    print(f"  Bot Gotinha — Laboratório de IA")
    print(f"  Modelo: {MODEL}")
    print(f"  'limpar' → novo contexto | 'sair' → encerrar")
    print(f"{'═' * 55}\n")

    historico: list[dict] = [{"role": "system", "content": SYSTEM_PROMPT}]
    turno = 0

    while True:
        try:
            pergunta = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nEncerrando. Até logo!")
            break

        if not pergunta:
            continue

        if pergunta.lower() == "sair":
            print("\nEncerrando. Até logo!")
            break

        if pergunta.lower() == "limpar":
            historico = [{"role": "system", "content": SYSTEM_PROMPT}]
            turno = 0
            print("\n[Contexto limpo. Nova conversa iniciada.]\n")
            continue

        turno += 1

        # Adiciona APENAS a pergunta do usuário por enquanto
        historico.append({"role": "user", "content": pergunta})

        try:
            resposta_final, resposta_raw, salvar, fora_tema = processar_turno(pergunta, historico)
        except Exception as e:
            print(f"\n[ERRO ao conectar ao Ollama: {e}]")
            print("Verifique se o Ollama está rodando: ollama serve\n")
            historico.pop()
            continue

        log_modelo(turno, pergunta, resposta_raw, resposta_final)
        print(f"\nAssistente: {resposta_final}\n")

        if salvar:
            # Turno sobre vacinação: salva resposta no histórico normalmente
            historico.append({"role": "assistant", "content": resposta_final})
        else:

            historico.pop()

            if DEBUG and fora_tema:

                print(
                    "[DEBUG] Turno fora do tema descartado do histórico.\n"
                )


if __name__ == "__main__":
    main()