# cobertura/dados.py

import os
import re
import html
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.normalizar import normalizar
from utils.estados import NOMES_ESTADOS


# ── Estado interno ────────────────────────────────────────────────────────────

_df: pd.DataFrame | None = None
_info_atualizacao: str | None = None

_BARRA = "─" * 40

_COLUNAS_IGNORAR = {
    " ", "Região Ocorrência", "UF Residência",
    "Macrorregião Saúde", "Região de Saúde",
    "Município Residência", "Imunobiológico",
}

_EXPLICACOES = {
    "< 30 Dias": "bebês até 30 dias",
    "<= 1 dia":  "1º dia de vida",
    "<= 2 dias":  "até 2 dias de vida",
}


# ── Download / Cache ──────────────────────────────────────────────────────────

def baixar_e_tratar_dados(
    pasta: str = "downloads",
    cache_segundos: int = 21600,
) -> pd.DataFrame:
    global _df, _info_atualizacao

    os.makedirs(pasta, exist_ok=True)
    caminho_xlsx = os.path.join(pasta, "cobertura_vacinal.xlsx")
    caminho_kpi  = os.path.join(pasta, "ultima_atualizacao.txt")

    def _expirado():
        if not os.path.exists(caminho_xlsx):
            return True
        return (time.time() - os.path.getmtime(caminho_xlsx)) > cache_segundos

    if _expirado():
        print("⬇️  Baixando dados do painel...")
        _baixar_via_selenium(pasta, caminho_xlsx, caminho_kpi)
    else:
        print("✅ Usando cache local.")
        if os.path.exists(caminho_kpi):
            with open(caminho_kpi, encoding="utf-8") as f:
                _info_atualizacao = f.read().strip()

    df = pd.read_excel(caminho_xlsx)
    df.columns = df.columns.str.strip()

    for col, fn in [
        ("UF Residência",        lambda s: s.astype(str).str.strip().str.upper()),
        ("Município Residência",  lambda s: s.astype(str).str.strip()),
        ("Macrorregião Saúde",   lambda s: s.astype(str).str.strip()),
        ("Região de Saúde",      lambda s: s.astype(str).str.strip()),
    ]:
        if col in df.columns:
            df[col] = fn(df[col])

    _df = df
    return _df


def carregar_dados() -> None:
    """Chamado pelo main.py na inicialização."""
    baixar_e_tratar_dados()


def _baixar_via_selenium(pasta: str, caminho_fixo: str, caminho_kpi: str) -> None:
    global _info_atualizacao

    opts = Options()
    opts.add_experimental_option("prefs", {
        "download.default_directory": os.path.abspath(pasta),
        "download.prompt_for_download": False,
    })

    driver = webdriver.Chrome(options=opts)
    wait   = WebDriverWait(driver, 20)

    try:
        driver.get(
            "https://infoms.saude.gov.br/extensions/"
            "SEIDIGI_DEMAS_VACINACAO_CALENDARIO_NACIONAL_COBERTURA_RESIDENCIA/"
            "SEIDIGI_DEMAS_VACINACAO_CALENDARIO_NACIONAL_COBERTURA_RESIDENCIA.html"
        )
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(5)

        kpi = driver.find_element(By.ID, "kpi-container").text
        m = re.search(r"Atualização do painel em (\d{2}/\d{2}/\d{4}) às (\d{2}:\d{2}:\d{2})", kpi)
        if m:
            _info_atualizacao = f"{m.group(1)} às {m.group(2)}"
            with open(caminho_kpi, "w", encoding="utf-8") as f:
                f.write(_info_atualizacao)

        driver.execute_script("arguments[0].click();", driver.find_element(By.ID, "aba2-tab"))
        time.sleep(3)
        driver.execute_script(
            "arguments[0].click();",
            driver.find_element(By.XPATH, "//div[contains(., 'Macrorregiões')]"),
        )
        time.sleep(3)
        driver.execute_script("arguments[0].click();", driver.find_element(By.ID, "exportar-dados-QV1-10"))
        print("⏳ Aguardando download...")
        time.sleep(10)
    finally:
        driver.quit()

    arquivos = sorted(
        [f for f in os.listdir(pasta) if f.endswith(".xlsx")],
        key=lambda x: os.path.getmtime(os.path.join(pasta, x)),
    )
    ultimo = os.path.join(pasta, arquivos[-1])
    if ultimo != caminho_fixo:
        if os.path.exists(caminho_fixo):
            os.remove(caminho_fixo)
        os.rename(ultimo, caminho_fixo)


# ── Helpers internos ──────────────────────────────────────────────────────────

def _get_df() -> pd.DataFrame:
    if _df is None:
        baixar_e_tratar_dados()
    return _df


def _to_float(valor) -> float | None:
    """Converte para float com segurança. Retorna None se não for número."""
    if valor is None or (isinstance(valor, float) and pd.isna(valor)):
        return None
    try:
        return float(valor)
    except (ValueError, TypeError):
        return None


def _coletar_percentuais(linha: pd.Series, df: pd.DataFrame) -> list[float]:
    """Retorna lista de percentuais (0–100) de todas as colunas de vacina."""
    resultado = []
    for col in df.columns:
        if col in _COLUNAS_IGNORAR:
            continue
        f = _to_float(linha[col])
        if f is not None and linha[col] != "-":
            resultado.append(round(f * 100, 2))
    return resultado


def _calcular_media(linha: pd.Series, df: pd.DataFrame) -> float | None:
    valores = _coletar_percentuais(linha, df)
    if not valores:
        return None
    return round(sum(valores) / len(valores), 2)


def _tratar_nome_vacina(nome: str) -> str:
    for chave, explicacao in _EXPLICACOES.items():
        if chave in nome:
            nome = nome.replace(chave, explicacao)
    return nome


def _rodape() -> str:
    if _info_atualizacao:
        return (
            f"\n{_BARRA}\n"
            f"<b>Última atualização:</b> {_info_atualizacao}\n"
            "Fonte: Rede Nacional de Dados em Saúde (RNDS)\n"
        )
    return ""


def _bloco_indicadores(valores: list[float], media: float) -> str:
    criticos = len([v for v in valores if v < 60])
    alertas  = len([v for v in valores if 60 <= v < 75])
    bloco    = "<b>Indicadores gerais</b>\n"
    bloco   += f"Média de cobertura: <b>{media}%</b>\n"
    if criticos:
        bloco += f"🚨 Vacinas críticas (abaixo de 60%): <b>{criticos}</b>\n"
    if alertas:
        bloco += f"⚠️ Em atenção (60–75%): <b>{alertas}</b>\n"
    return bloco


def _bloco_detalhamento(linha: pd.Series, df: pd.DataFrame) -> str:
    bloco = f"\n{_BARRA}\n<b>Detalhamento por vacina</b>\n\n"
    for col in df.columns:
        if col in _COLUNAS_IGNORAR:
            continue
        f = _to_float(linha[col])
        if f is None or linha[col] == "-":
            continue
        pct = round(f * 100, 2)
        if pct < 60:
            cor, status = "🔴", "— 🚨 Crítico"
        elif pct < 75:
            cor, status = "🟡", "— ⚠️ Atenção"
        else:
            cor, status = "🟢", ""
        nome = html.escape(_tratar_nome_vacina(col))
        bloco += f"{cor} {nome}: <b>{pct}%</b> {status}\n\n"
    return bloco


# ── Busca por Estado ──────────────────────────────────────────────────────────

def buscar_cobertura_estado(uf: str) -> str:
    df = _get_df()
    uf = uf.upper()

    df_uf = df[
        (df["UF Residência"] == uf) &
        (df["Macrorregião Saúde"] == "Totais")
    ]
    if df_uf.empty:
        return "❌ Estado não encontrado."

    linha  = df_uf.iloc[0]
    media  = _calcular_media(linha, df)
    if media is None:
        return "⚠️ Não foi possível calcular a cobertura."

    valores = _coletar_percentuais(linha, df)

    # Média Brasil (coluna " " com valor "Brasil")
    media_brasil = None
    if " " in df.columns:
        df_br = df[df[" "].astype(str).str.strip() == "Brasil"]
        if not df_br.empty:
            media_brasil = _calcular_media(df_br.iloc[0], df)

    nome = html.escape(NOMES_ESTADOS.get(uf, uf))

    resposta  = f"<b>📍 COBERTURA VACINAL — {nome} ({uf})</b>\n{_BARRA}\n\n"
    resposta += _bloco_indicadores(valores, media)
    resposta += _bloco_detalhamento(linha, df)
    resposta += f"\n{_BARRA}\n"
    resposta += "Cobertura ideal recomendada: <b>acima de 90%</b>\n"

    if media_brasil is not None:
        resposta += f"\n{_BARRA}\n<b>Comparação nacional</b>\n"
        resposta += f"{nome}: <b>{media}%</b>  |  Brasil: <b>{media_brasil}%</b>\n"
        if media < media_brasil:
            resposta += "📉 Abaixo da média nacional"
        elif media > media_brasil:
            resposta += "📈 Acima da média nacional"
        else:
            resposta += "➡️ Alinhado à média nacional"

    resposta += _rodape()
    return resposta


# ── Busca por Município ───────────────────────────────────────────────────────

def buscar_cobertura_municipio(uf: str, municipio: str) -> str:
    df  = _get_df()
    uf  = uf.upper()
    mun_norm = normalizar(municipio)

    # No Excel: "350950 - Campinas"
    df_uf = df[
        (df["UF Residência"] == uf) &
        (df["Município Residência"].str.match(r"^\d{6}\s*-\s*", na=False))
    ]

    mask   = df_uf["Município Residência"].apply(
        lambda x: normalizar(x.split(" - ", 1)[-1]) == mun_norm
    )
    df_mun = df_uf[mask]

    if df_mun.empty:
        return _sugerir_municipios(uf, municipio, df_uf)

    linha     = df_mun.iloc[0]
    nome_mun  = linha["Município Residência"].split(" - ", 1)[-1].strip()
    media     = _calcular_media(linha, df)

    if media is None:
        return f"⚠️ Sem dados de cobertura para {municipio} / {uf}."

    valores     = _coletar_percentuais(linha, df)
    nome_estado = html.escape(NOMES_ESTADOS.get(uf, uf))
    mun_safe    = html.escape(nome_mun)

    resposta  = f"<b>📍 COBERTURA VACINAL — {mun_safe} / {nome_estado}</b>\n{_BARRA}\n\n"
    resposta += _bloco_indicadores(valores, media)
    resposta += _bloco_detalhamento(linha, df)
    resposta += f"\n{_BARRA}\n"
    resposta += "Cobertura ideal recomendada: <b>acima de 90%</b>\n"
    resposta += _rodape()
    return resposta


def _sugerir_municipios(uf: str, municipio: str, df_uf: pd.DataFrame) -> str:
    mun_norm  = normalizar(municipio)
    nomes     = [x.split(" - ", 1)[-1].strip() for x in df_uf["Município Residência"].dropna()]
    sugestoes = [n for n in nomes if mun_norm in normalizar(n)][:5]
    msg = f"❌ Município <b>{html.escape(municipio)}</b> não encontrado em {uf}.\n\n"
    if sugestoes:
        msg += "🔍 Você quis dizer?\n"
        for s in sugestoes:
            msg += f"  • {html.escape(s)}\n"
    else:
        msg += "Verifique o nome e tente novamente."
    return msg


# ── Detecção de município no texto livre ──────────────────────────────────────

def detectar_municipio(texto: str) -> tuple[str, str] | None:
    """
    Varre o DataFrame procurando qualquer município cujo nome apareça no texto.
    Retorna (nome_limpo, uf) ou None.
    """
    df        = _get_df()
    texto_norm = normalizar(texto)

    df_muns = df[df["Município Residência"].str.match(r"^\d{6}\s*-\s*", na=False)]

    for _, row in df_muns.iterrows():
        raw  = str(row["Município Residência"])
        nome = raw.split(" - ", 1)[-1].strip()
        if normalizar(nome) in texto_norm:
            uf = str(row["UF Residência"]).strip().upper()
            return nome, uf

    return None


# ── Ranking ───────────────────────────────────────────────────────────────────

def ranking_estados() -> str:
    df = _get_df()

    df_totais = df[
        (df["UF Residência"].notna()) &
        (df["UF Residência"] != "") &
        (df["UF Residência"] != "NAN") &
        (df["Macrorregião Saúde"] == "Totais") &
        (df["Região de Saúde"].isin(["", "nan", "NAN"]) | df["Região de Saúde"].isna())
    ]

    medias = []
    for _, linha in df_totais.iterrows():
        uf    = str(linha.get("UF Residência", "")).strip()
        media = _calcular_media(linha, df)
        if uf and media is not None:
            medias.append((uf, media))

    if not medias:
        return "⚠️ Não foi possível gerar o ranking."

    ranking      = sorted(medias, key=lambda x: x[1], reverse=True)
    media_brasil = round(sum(m for _, m in ranking) / len(ranking), 2)

    medalhas = {1: "🥇", 2: "🥈", 3: "🥉"}
    resposta  = f"<b>🇧🇷 COBERTURA VACINAL — RANKING POR ESTADO</b>\n{_BARRA}\n\n"

    for i, (uf, media) in enumerate(ranking, start=1):
        prefixo = medalhas.get(i, f"{i:>2}.")
        nome    = html.escape(NOMES_ESTADOS.get(uf, uf))
        cor     = "🔴" if media < 60 else ("🟡" if media < 75 else "🟢")
        resposta += f"{prefixo} {cor} {uf} — {nome}: <b>{media}%</b>\n\n"

    resposta += f"\n{_BARRA}\n<b>Média geral Brasil: {media_brasil}%</b>\n"
    resposta += _rodape()
    return resposta