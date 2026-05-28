# utils.py
# Funções utilitárias puras: parsing, normalização, filtros, detecção e logging.
# Nenhuma chamada ao modelo ou ao database acontece aqui.

import re
import unicodedata
from datetime import datetime


# ── Normalização ──────────────────────────────────────────────────────────────

def normalizar(texto: str) -> str:
    """Remove acentos, converte para minúsculas e elimina espaços extras."""
    if not texto:
        return ""
    texto = texto.strip().lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto


# ── Parsing da Resposta do Modelo ─────────────────────────────────────────────

def parse_resposta_modelo(resposta: str) -> dict:
    """
    Interpreta a resposta bruta do modelo.

    Retorna um dicionário com:
      - tipo: "tool" | "texto"
      - tool: nome da ferramenta (se tipo == "tool")
      - parametro: parâmetro da ferramenta (se tipo == "tool")
      - texto: resposta livre (se tipo == "texto")
      - raw: string original recebida
    """
    raw = resposta.strip().strip("`").strip()

    if raw.upper().startswith("CALL_TOOL"):
        partes = raw.split(":", 2)

        if len(partes) < 2:
            return {"tipo": "texto", "texto": raw, "raw": raw}

        tool = partes[1].strip()
        parametro = partes[2].strip() if len(partes) > 2 else ""

        if parametro.lower() in ("none", ""):
            parametro = ""

        return {
            "tipo": "tool",
            "tool": tool,
            "parametro": parametro,
            "raw": raw,
        }

    return {"tipo": "texto", "texto": raw, "raw": raw}


# ── Extração de Idade ─────────────────────────────────────────────────────────

def extrair_idade(pergunta: str) -> int | None:
    """
    Tenta extrair idade da pergunta.
    Aceita: "18 anos", "18 anos de idade", "nascido em 15 de março de 1990".
    Retorna int ou None se não encontrar.
    """
    pergunta = normalizar(pergunta)

    match_anos = re.search(r"(\d{1,3})\s+anos?", pergunta)
    if match_anos:
        return int(match_anos.group(1))

    match_data = re.search(r"\d{1,2}\s+de\s+\w+\s+de\s+(\d{4})", pergunta)
    if match_data:
        ano_nascimento = int(match_data.group(1))
        return datetime.now().year - ano_nascimento

    return None


# ── Filtro de Saudação ────────────────────────────────────────────────────────

_SAUDACOES = {
    "oi", "ola", "opa", "eae", "bom dia", "boa tarde",
    "boa noite", "salve", "hello", "hi", "hey",
}


def pergunta_e_saudacao(pergunta: str) -> bool:
    """Retorna True se a pergunta for apenas uma saudação."""
    return normalizar(pergunta) in _SAUDACOES


# ── Filtro de Tema ────────────────────────────────────────────────────────────
# Perguntas que não baterem em nenhum desses padrões são bloqueadas pelo Python,
# sem nem chegar ao modelo.

_PADROES_TEMA_VACINA = [
    r"\bvacin",       r"\bimuniza",     r"\bimunidade\b",
    r"\bcobertura\b", r"\bposto\b",     r"\bubs\b",
    r"\bsus\b",       r"\bsaude\b",     r"\binfec",
    r"\bdoenca\b",    r"\bpreven",      r"\befeito\b",
    r"\bcolateral\b", r"\baplicac",     r"\bdose\b",
    r"\breforco\b",   r"\bcalendario\b",r"\bendereco\b",
    r"\bhorario\b",   r"\bgripe\b",     r"\binfluenza\b",
    r"\bcovid\b",     r"\bhpv\b",       r"\bbcg\b",
    r"\bhepatite\b",  r"\bfebre amarela\b", r"\bpolio\b",
    r"\bpneumo\b",    r"\btetano\b",    r"\bsarampo\b",
    r"\bdtpa?\b",     r"\bmeningit",    r"\bvaricel",
    r"\brotavir",     r"\bgestante\b",  r"\bgestacao\b",
    r"\bidoso\b",     r"\bcrianca\b",   r"\badolescente\b",
    r"\brecem.nascido\b", r"\bpandemia\b", r"\bepidemia\b",
    r"\banticorpo\b", r"\branking\b",   r"\bpior\b",
    r"\bmelhor\b",    r"\badulto\b",
]

_PATTERN_TEMA = re.compile("|".join(_PADROES_TEMA_VACINA), re.IGNORECASE)


def pergunta_e_sobre_vacina(pergunta: str) -> bool:
    """Retorna True se a pergunta tiver relação com vacinação ou saúde pública."""
    return bool(_PATTERN_TEMA.search(normalizar(pergunta)))


# ── Gatilhos de Necessidade de Dados ─────────────────────────────────────────
# Se a pergunta bater aqui e o modelo não chamar CALL_TOOL → aciona retry.

_PADROES_GATILHO_DADOS = [
    r"\bcobertura\b",       r"\bpercentual\b",        r"\branking\b",
    r"\bpior\b",            r"\bmelhor\b",
    r"\bvacinas?\s+(para|de|por|recomendadas?)\b",
    r"\brecomendadas?\s+para\b", r"\bquais\s+vacinas?\b",
    r"\befeitos?\s+colaterais?\s+da\b",
    r"\breacoes?\s+da\s+vacina\b",
    r"\bendereco\b",        r"\bposto\b",             r"\bhorario\b",
    r"\bidade\b",           r"\banos?\b",
    r"\bidosos?\b",         r"\bgestantes?\b",
    r"\bcriancas?\b",       r"\badolescentes?\b",      r"\badultos?\b",
]

_PATTERN_DADOS = re.compile("|".join(_PADROES_GATILHO_DADOS), re.IGNORECASE)


def pergunta_quer_dados(pergunta: str) -> bool:
    """Retorna True se a pergunta provavelmente precisar de uma tool."""
    return bool(_PATTERN_DADOS.search(normalizar(pergunta)))


# ── Detecção de Alucinação ────────────────────────────────────────────────────

_VACINAS_CONHECIDAS = re.compile(
    r"\b(bcg|hepatite b|hepatite a|influenza|hpv|dtpa|dtp|poliomielite|sarampo|"
    r"triplice viral|febre amarela|pneumococica|meningococica|varicela|rotavirus)\b",
    re.IGNORECASE,
)


def resposta_parece_alucinacao(texto: str) -> bool:
    """
    Detecta sinais de que o modelo inventou dados.
      - Percentual numérico → inventou cobertura
      - 5+ vacinas distintas listadas → inventou lista
    """
    if re.search(r"\b\d{1,3}%", texto):
        return True

    vacinas = _VACINAS_CONHECIDAS.findall(texto)
    if len({v.lower() for v in vacinas}) >= 5:
        return True

    return False


# ── Contexto de Follow-up ─────────────────────────────────────────────────────
# Verifica apenas mensagens do USUÁRIO — mensagens do assistente
# podem conter palavras de vacinação e contaminar o filtro.

_PALAVRAS_FOLLOWUP = [
    "cobertura", "vacina", "imuniza", "posto", "ubs", "efeito",
    "colateral", "dose", "grupo", "idade", "ranking", "estado",
    "cidade", "gripe", "covid", "hpv", "bcg", "hepatite", "influenza",
    "gestante", "idoso", "crianca", "adolescente", "adulto",
]


def tem_contexto_vacina_no_historico(historico: list[dict], janela: int = 4) -> bool:
    """
    Retorna True se alguma das últimas `janela` mensagens do USUÁRIO
    contiver palavras relacionadas a vacinação.
    Permite que follow-ups curtos como "e do Rio?" sejam aceitos.
    """
    msgs_usuario = [m for m in historico if m["role"] == "user"][-janela:]
    return any(
        kw in normalizar(msg["content"])
        for msg in msgs_usuario
        for kw in _PALAVRAS_FOLLOWUP
    )


# ── Sanitização do Histórico ──────────────────────────────────────────────────

def historico_sanitizado(historico: list[dict]) -> list[dict]:
    """
    Remove perguntas de volta do assistente que possam confundir o modelo.
    Perguntas curtas do assistente (< 120 chars, terminando em '?')
    são substituídas por um placeholder neutro.
    """
    resultado = []
    for msg in historico:
        if msg["role"] == "assistant":
            texto = msg["content"].strip()
            eh_pergunta_curta = texto.endswith("?") and len(texto) < 120
            nao_e_call_tool = not texto.upper().startswith("CALL_TOOL")
            if eh_pergunta_curta and nao_e_call_tool:
                msg = {"role": "assistant", "content": "[aguardando informação do usuário]"}
        resultado.append(msg)
    return resultado


# ── Logging ───────────────────────────────────────────────────────────────────

def log_turno(turno: int, pergunta: str, resposta_raw: str, resultado: str) -> None:
    """Log estruturado por turno para comparação de modelos."""
    sep = "─" * 52
    print(f"\n{sep}")
    print(f"[TURNO {turno}]")
    print(f"  Pergunta  : {pergunta}")
    print(f"  Modelo raw: {resposta_raw}")
    print(f"  Resultado : {resultado}")
    print(sep)