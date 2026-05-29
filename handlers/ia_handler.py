# handlers/ia_handler.py

import re
import ollama
from datetime import datetime

from prompts import SYSTEM_PROMPT, PROMPT_CLASSIFICADOR
from handlers.faq import buscar_faq

from cobertura.dados import (
    buscar_cobertura_estado,
    buscar_cobertura_municipio,
    detectar_municipio,
    ranking_estados,
)
from vacinas.dados import (
    buscar_vacinas_por_idade,
    buscar_vacinas_por_grupo,
    formatar_lista_vacinas,
)
from utils.estados import detectar_estado, NOMES_ESTADOS
from utils.normalizar import normalizar

MODEL = "llama3.2:latest"
ANO_ATUAL = datetime.now().year


# ── Filtro de tema ────────────────────────────────────────────────────────────
# Se NENHUM desses padrões bater, a mensagem é bloqueada antes de qualquer
# chamada ao modelo. Isso garante que futebol, piadas, política, etc.
# nunca sejam respondidos.

_SAUDACOES = {
    "oi",
    "ola",
    "opa",
    "eae",
    "ei",
    "iae",
    "hello",
    "hi",
    "hey",
    "bom dia",
    "boa tarde",
    "boa noite",
    "boas",
    "salve",
    "tudo bem",
    "tudo bom",
    "como vai",
    "boa",
    "bão",
}

_PADROES_SAUDE = re.compile(
    r"\b("
    # vacinação / imunização
    r"vacin|imuniz|imunidad|cobertura|calendari|carteira de vacin|caderneta"
    r"|dose|reforco|reforcinho|aplicacao|aplicar|tomar|deve tomar|precisa tomar"
    r"|vacinar|vacinado|vacinada|vacinar"
    r"|repouso|reacao|reação|efeito|efeitos"
    # doenças / prevenção
    r"|doenca|virus|bacteria|infeccao|epidemia|pandemia|prevencao|prevenir"
    r"|sarampo|polio|gripe|influenza|covid|hepatite|hpv|bcg|tetano|dengue"
    r"|febre amarela|meningite|pneumo|rotavir|varicela|caxumba|rubeola|difteria|coqueluche"
    # saúde geral
    r"|saude|sus|ubs|posto de saude|hospital|clinica|medico|enfermeiro|farmacia"
    r"|consulta|atendimento|tratamento|medicamento|remedio|prescricao"
    r"|sintoma|febre|dor|reacao|efeito colateral|alergia|inflamacao"
    r"|gestante|gravida|gestacao|gravidez|bebe|recem.nascido|crianca|criança|filho|filha|idoso|idosa"
    r"|sistema imunologico|anticorpo|anticorpos|imune|imunidade"
    # dados / ranking
    r"|ranking|cobertura vacinal|percentual|indice|dado|estatistica" r")\b",
    re.IGNORECASE,
)


def _e_saudacao(texto: str) -> bool:
    return normalizar(texto) in _SAUDACOES


def _e_sobre_saude(texto: str) -> bool:
    return bool(_PADROES_SAUDE.search(normalizar(texto)))


def _bloqueado(texto: str) -> bool:
    """Retorna True se a mensagem deve ser bloqueada (fora do tema)."""
    return not _e_saudacao(texto) and not _e_sobre_saude(texto)


# ── Extração de idade ─────────────────────────────────────────────────────────


def _extrair_idade(texto: str) -> int | None:
    t = texto.lower()

    # "tenho 19 anos" / "19 anos de idade"
    m = re.search(r"\b(\d{1,3})\s+anos?\b", t)
    if m:
        return int(m.group(1))

    # "nasci em 2003" / "ano de nascimento 2003"
    m = re.search(r"\b(19\d{2}|20[0-2]\d)\b", t)
    if m:
        return ANO_ATUAL - int(m.group(1))

    # "15/06/2003" ou "15-06-2003"
    m = re.search(r"\b\d{1,2}[/\-]\d{2}[/\-](19\d{2}|20[0-2]\d)\b", t)
    if m:
        return ANO_ATUAL - int(m.group(1))

    return None


# ── Classificador Python-first ────────────────────────────────────────────────


def classificar(texto: str) -> tuple[str, dict]:
    """
    Ordem de prioridade:
      1. Saudação
      2. FAQ (resposta estática)
      3. Ranking
      4. Vacinas por idade
      5. Município detectado no DataFrame
      6. Estado + cobertura
      7. Cobertura sem local
      8. Fallback IA (apenas para perguntas de saúde já validadas)
    """
    lower = texto.lower()

    # 1. Saudação
    if _e_saudacao(texto):
        return "SAUDACAO", {}

    # 2. FAQ
    resposta_faq = buscar_faq(texto)
    if resposta_faq:
        return "FAQ", {"resposta": resposta_faq}

    # 3. Ranking
    _RANKING_KW = (
        "ranking",
        "melhor estado",
        "pior estado",
        "todos os estados",
        "lista de estados",
        "comparar estados",
    )
    if any(kw in lower for kw in _RANKING_KW):
        return "RANKING", {}

    _GRUPOS_MAP = {
        "idoso": "idosos",
        "idosos": "idosos",
        "gestante": "gestantes",
        "gestantes": "gestantes",
        "crianca": "criancas",
        "crianças": "criancas",
        "criancas": "criancas",
        "adolescente": "adolescentes",
        "adolescentes": "adolescentes",
        "adulto": "adultos",
        "adultos": "adultos",
        "imunossuprimido": "imunossuprimidos",
        "imunossuprimidos": "imunossuprimidos",
        "profissional de saude": "profissionais de saude",
        "profissionais de saude": "profissionais de saude",
    }

    # 4. Vacinas por idade
    _VACINA_KW = (
        "vacina",
        "tomar",
        "devo tomar",
        "preciso tomar",
        "vacinar",
        "calendario",
        "calendário",
        "imunizacao",
        "imunização",
    )
    idade = _extrair_idade(texto)
    if idade is not None and any(kw in lower for kw in _VACINA_KW):
        return "VACINA_IDADE", {"idade": idade}

        # 5. Vacinas por grupo
    for palavra, grupo in _GRUPOS_MAP.items():

        if palavra in normalizar(lower):

            if any(kw in lower for kw in _VACINA_KW):
                return "VACINA_GRUPO", {"grupo": grupo}

    # 6. Município
    resultado_mun = detectar_municipio(texto)
    if resultado_mun:
        municipio, uf = resultado_mun
        return "COBERTURA_MUNICIPIO", {"municipio": municipio, "uf": uf}

    # 6. Estado + cobertura
    _COBERTURA_KW = (
        "cobertura",
        "vacinacao",
        "vacinação",
        "imunizacao",
        "imunização",
        "indice",
        "índice",
    )
    uf = detectar_estado(texto)
    if uf and any(kw in lower for kw in _COBERTURA_KW):
        return "COBERTURA_ESTADO", {"uf": uf}

    # 7. Cobertura sem local
    if any(kw in lower for kw in _COBERTURA_KW):
        return "COBERTURA", {}

    # 8. Fallback IA — só chega aqui se _e_sobre_saude() já validou
    resp = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": PROMPT_CLASSIFICADOR},
            {"role": "user", "content": texto},
        ],
        options={"temperature": 0, "num_predict": 20},
    )
    intencao = resp["message"]["content"].strip().upper().split()[0]
    return intencao, {}


# ── Envio com paginação ───────────────────────────────────────────────────────


def _enviar(bot, chat_id: int, texto: str) -> None:
    for i in range(0, len(texto), 4000):
        bot.send_message(chat_id, texto[i : i + 4000], parse_mode="HTML")


# ── Resposta livre pela IA ────────────────────────────────────────────────────


def _responder_ia(pergunta: str) -> str:
    resp = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": pergunta},
        ],
        options={"temperature": 0.3, "num_predict": 300},
    )
    return resp["message"]["content"].strip()


# ── Mensagem de bloqueio ──────────────────────────────────────────────────────

_MSG_FORA_TEMA = (
    "Só consigo ajudar com assuntos de <b>vacinação e saúde pública</b>. 💉\n\n"
    "Posso responder sobre:\n"
    "• Cobertura vacinal por estado ou município\n"
    "• Vacinas por idade ou grupo\n"
    "• Calendário vacinal\n"
    "• Dúvidas sobre vacinas e o SUS"
)


# ── Roteamento ────────────────────────────────────────────────────────────────


def processar_mensagem(bot, msg) -> None:
    texto = msg.text.strip()

    # Bloqueia fora do tema antes de qualquer processamento
    if _bloqueado(texto):
        print(f"[BLOQUEADO] '{texto[:60]}'")
        bot.reply_to(msg, _MSG_FORA_TEMA, parse_mode="HTML")
        return

    try:
        intencao, ctx = classificar(texto)
        print(f"[IA] {intencao} | ctx={ctx} | '{texto[:60]}'")

        match intencao:

            case "SAUDACAO":
                bot.reply_to(
                    msg,
                    "Olá! 👋 Sou o <b>Assistente Gotinha</b> 💉\n\n"
                    "Posso ajudar com:\n"
                    "• Cobertura vacinal por estado ou município\n"
                    "• Ranking nacional\n"
                    "• Vacinas por idade ou grupo\n"
                    "• Dúvidas sobre vacinação e o SUS",
                    parse_mode="HTML",
                )

            case "FAQ":
                bot.send_message(msg.chat.id, ctx["resposta"], parse_mode="HTML")

            case "RANKING":
                _enviar(bot, msg.chat.id, ranking_estados())

            case "VACINA_IDADE":
                idade = ctx["idade"]
                vacinas = buscar_vacinas_por_idade(idade)
                resposta = formatar_lista_vacinas(
                    f"💉 Vacinas recomendadas para <b>{idade} anos</b>:", vacinas
                )
                bot.send_message(msg.chat.id, resposta, parse_mode="HTML")

            case "VACINA_GRUPO":

                grupo = ctx["grupo"]

                vacinas = buscar_vacinas_por_grupo(
                    grupo
                )

                resposta = formatar_lista_vacinas(
                    f"💉 Vacinas para {grupo}:",
                    vacinas
                )

                bot.send_message(
                    msg.chat.id,
                    resposta,
                    parse_mode="HTML"
                )

            case "COBERTURA_MUNICIPIO":
                _enviar(
                    bot,
                    msg.chat.id,
                    buscar_cobertura_municipio(ctx["uf"], ctx["municipio"]),
                )

            case "COBERTURA_ESTADO":
                uf = ctx.get("uf") or detectar_estado(texto)
                if not uf:
                    bot.reply_to(msg, "⚠️ Não consegui identificar o estado.")
                    return
                _enviar(bot, msg.chat.id, buscar_cobertura_estado(uf))

            case "COBERTURA":
                bot.reply_to(
                    msg,
                    "📊 Para consultar cobertura, me diga o local:\n\n"
                    "• <b>cobertura SP</b>\n"
                    "• <b>cobertura São Paulo</b>\n"
                    "• <b>cobertura Campinas</b>\n\n"
                    "Ou use o menu 👇",
                    parse_mode="HTML",
                )

            case "VACINA":
                _enviar(bot, msg.chat.id, _responder_ia(texto))

            case "FORA_CONTEXTO":
                bot.reply_to(msg, _MSG_FORA_TEMA, parse_mode="HTML")

            case _:
                _enviar(bot, msg.chat.id, _responder_ia(texto))

    except Exception as e:
        import traceback

        print(f"[ERRO ia_handler]: {e}")
        traceback.print_exc()
        bot.reply_to(msg, "⚠️ Erro ao processar sua mensagem. Tente novamente.")
