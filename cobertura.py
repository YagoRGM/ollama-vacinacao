import pandas as pd

df = None

# =========================
# CARREGAR
# =========================

def carregar_dados():

    global df

    df = pd.read_csv(
        "downloads/cobertura_vacinal.xlsx"
    )

# =========================
# ESTADO
# =========================

def buscar_cobertura_estado(uf):

    dados = df[
        df["UF"] == uf
    ]

    if dados.empty:
        return "Estado não encontrado."

    media = round(
        dados["COBERTURA"].mean(),
        2
    )

    return (
        f"📍 Estado: {uf}\n"
        f"💉 Cobertura Vacinal: {media}%"
    )

# =========================
# MUNICÍPIO
# =========================

def buscar_cobertura_municipio(
    uf,
    municipio
):

    dados = df[
        (df["UF"] == uf)
        &
        (
            df["MUNICIPIO"]
            .str.upper()
            ==
            municipio.upper()
        )
    ]

    if dados.empty:
        return "Município não encontrado."

    cobertura = dados.iloc[0]["COBERTURA"]

    return (
        f"📍 Município: {municipio}\n"
        f"🏛️ Estado: {uf}\n"
        f"💉 Cobertura: {cobertura}%"
    )

# =========================
# DETECTAR MUNICÍPIO
# =========================

def detectar_municipio(texto):

    texto = texto.upper()

    municipios = (
        df["MUNICIPIO"]
        .dropna()
        .unique()
    )

    for municipio in municipios:

        if municipio.upper() in texto:
            return municipio

    return None

# =========================
# PEGAR UF
# =========================

def obter_estado_do_municipio(
    municipio
):

    dados = df[
        df["MUNICIPIO"]
        .str.upper()
        ==
        municipio.upper()
    ]

    if dados.empty:
        return None

    return dados.iloc[0]["UF"]

# =========================
# RANKING
# =========================

def ranking_estados():

    ranking = (
        df
        .groupby("UF")["COBERTURA"]
        .mean()
        .reset_index()
    )

    ranking = ranking.sort_values(
        by="COBERTURA",
        ascending=False
    )

    media_brasil = round(
        ranking["COBERTURA"].mean(),
        2
    )

    texto = (
        "🇧🇷 RANKING NACIONAL\n\n"
    )

    medalhas = [
        "🥇",
        "🥈",
        "🥉"
    ]

    for i, row in ranking.iterrows():

        uf = row["UF"]
        media = round(
            row["COBERTURA"],
            2
        )

        if i < 3:
            emoji = medalhas[i]
        else:
            emoji = "📍"

        texto += (
            f"{emoji} {uf} — "
            f"{media}%\n"
        )

    texto += (
        f"\n🇧🇷 Média do Brasil: "
        f"{media_brasil}%"
    )

    return texto