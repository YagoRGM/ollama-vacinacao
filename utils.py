# utils.py

import unicodedata
import re


def normalizar(texto: str) -> str:
    """Remove acentos, minúsculas, espaços extras."""
    if not texto:
        return ""
    texto = texto.strip().lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto


def parse_resposta_modelo(resposta: str) -> dict:
    """
    Interpreta a resposta do modelo de forma robusta.
    Retorna dict com: tipo, tool, parametro, texto, raw
    """
    raw = resposta.strip()
    raw_limpo = raw.strip("`").strip()

    if raw_limpo.upper().startswith("CALL_TOOL"):
        partes = raw_limpo.split(":", 2)
        if len(partes) < 2:
            return {"tipo": "texto", "texto": raw, "raw": raw}

        tool = partes[1].strip()
        parametro = partes[2].strip() if len(partes) > 2 else ""

        if parametro.lower() in ("none", ""):
            parametro = ""

        return {"tipo": "tool", "tool": tool, "parametro": parametro, "raw": raw}

    return {"tipo": "texto", "texto": raw, "raw": raw}


# ── Filtro de tema ────────────────────────────────────────────────────────────
# Palavras que indicam que a pergunta É sobre vacinação/saúde pública.
# Se NENHUMA bater → bloquear antes mesmo de consultar o modelo.
_TEMA_VACINA = [
    r"\bvacin",
    r"\bimuniza",
    r"\bimunidade\b",
    r"\bcobertura\b",
    r"\bposto\b",
    r"\bubs\b",
    r"\bsus\b",
    r"\bsaude\b",          # saúde / saude
    r"\binfec",
    r"\bdoenca\b",         # doença / doenca
    r"\bpreven",
    r"\befeito\b",
    r"\bcolateral\b",
    r"\baplicac",          # aplicação
    r"\bdose\b",
    r"\breforco\b",        # reforço
    r"\bcalendario\b",     # calendário
    r"\bendereco\b",       # endereço
    r"\bhorario\b",        # horário
    r"\bgripe\b",
    r"\binfluenza\b",
    r"\bcovid\b",
    r"\bhpv\b",
    r"\bbcg\b",
    r"\bhepatite\b",
    r"\bfebre amarela\b",
    r"\bpolio\b",
    r"\bpneumo\b",
    r"\btetano\b",
    r"\bsarampo\b",
    r"\bdtpa?\b",
    r"\bmeningit",
    r"\bvaricel",
    r"\brotavir",
    r"\bgestante\b",
    r"\bgestacao\b",        # gestação
    r"\bidoso\b",
    r"\bcrianca\b",         # criança
    r"\badolescente\b",
    r"\brecem.nascido\b",   # recém-nascido
    r"\bpandemia\b",
    r"\bepidemia\b",
    r"\banticorpo\b",
    r"\branking\b",
    r"\bpior\b",
    r"\bmelhor\b",
    r"\badulto\b",
]

_PATTERN_TEMA = re.compile("|".join(_TEMA_VACINA), re.IGNORECASE)


def pergunta_e_sobre_vacina(pergunta: str) -> bool:
    """
    Retorna True se a pergunta tem relação com vacinação/saúde pública.
    Filtro aplicado ANTES de consultar o modelo.
    Conservador: qualquer dúvida → deixa passar (False negative é melhor que bloquear erroneamente).
    """
    return bool(_PATTERN_TEMA.search(normalizar(pergunta)))


# ── Gatilhos de dados ─────────────────────────────────────────────────────────
# Se a pergunta bater aqui e o modelo não chamar CALL_TOOL → retry
_GATILHOS_DADOS = [
    r"\bcobertura\b",
    r"\bpercentual\b",
    r"\branking\b",
    r"\bpior\b",
    r"\bmelhor\b",
    r"\bvacinas?\s+(para|de|por|recomendadas?)\b",
    r"\brecomendadas?\s+para\b",
    r"\bquais\s+vacinas?\b",
    r"\befeitos?\s+colaterais?\b",
    r"\bendereco\b",
    r"\bposto\b",
    r"\bhorario\b",
    r"\bidade\b",
    r"\banos?\b",
    r"\bidoso\b",
    r"\bgestante\b",
    r"\bcrianca\b",
    r"\badolescente\b",
    r"\badulto\b",
    r"\bgripe\b",
    r"\binfluenza\b",
    r"\bcovid\b",
    r"\bhpv\b",
    r"\bbcg\b",
    r"\bhepatite\b",
    r"\bfebre amarela\b",
    r"\bpolio\b",
    r"\bpneumo\b",
    r"\btetano\b",
    r"\bsarampo\b",
    r"\bdtpa?\b",
]

_PATTERN_DADOS = re.compile("|".join(_GATILHOS_DADOS), re.IGNORECASE)


def pergunta_quer_dados(pergunta: str) -> bool:
    """Retorna True se a pergunta provavelmente precisa de uma tool."""
    return bool(_PATTERN_DADOS.search(normalizar(pergunta)))


def resposta_parece_alucinacao(texto: str) -> bool:
    """Detecta se uma resposta livre parece conter dados inventados."""
    # Percentual numérico → modelo inventou cobertura
    if re.search(r"\b\d{1,3}%", texto):
        return True
    # 3+ vacinas distintas listadas → modelo inventou lista
    vacinas_encontradas = re.findall(
        r"\b(bcg|hepatite b|hepatite a|influenza|hpv|dtpa|dtp|poliomielite|sarampo|"
        r"triplice viral|febre amarela|pneumococica|meningococica|varicela|rotavirus)\b",
        texto, re.IGNORECASE
    )
    if len(set(v.lower() for v in vacinas_encontradas)) >= 3:
        return True
    return False


def historico_sanitizado(historico: list[dict]) -> list[dict]:
    """Remove 'perguntas de volta' do assistente que contaminam o contexto."""
    resultado = []
    for msg in historico:
        if msg["role"] == "assistant":
            texto = msg["content"].strip()
            eh_pergunta_curta = texto.endswith("?") and len(texto) < 120
            eh_call_tool = texto.upper().startswith("CALL_TOOL")
            if eh_pergunta_curta and not eh_call_tool:
                msg = {"role": "assistant", "content": "[aguardando informação do usuário]"}
        resultado.append(msg)
    return resultado


def log_modelo(turno: int, pergunta: str, resposta_raw: str, resultado: str, retry: bool = False):
    """Log estruturado por turno para análise comparativa de modelos."""
    sep = "─" * 52
    retry_label = " [RETRY]" if retry else ""
    print(f"\n{sep}")
    print(f"[TURNO {turno}{retry_label}]")
    print(f"  Pergunta  : {pergunta}")
    print(f"  Modelo raw: {resposta_raw}")
    print(f"  Resultado : {resultado}")
    print(sep)