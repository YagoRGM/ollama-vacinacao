# cobertura.py

import os
import time
import pandas as pd
import unicodedata

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# cache global
df_global = None

# pasta downloads
PASTA_DOWNLOAD = "downloads"

# cria pasta se não existir
os.makedirs(PASTA_DOWNLOAD, exist_ok=True)

CAMINHO_EXCEL = os.path.join(
    PASTA_DOWNLOAD,
    "cobertura_vacinal.xlsx"
)

URL = "https://infoms.saude.gov.br/extensions/SEIDIGI_DEMAS_VACINACAO_CALENDARIO_NACIONAL_COBERTURA_RESIDENCIA/SEIDIGI_DEMAS_VACINACAO_CALENDARIO_NACIONAL_COBERTURA_RESIDENCIA.html"


def baixar_excel():

    print("Baixando dados...")

    options = Options()

    prefs = {
        "download.default_directory": os.path.abspath(PASTA_DOWNLOAD),
        "download.prompt_for_download": False,
    }

    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get(URL)

    time.sleep(10)

    # =========================
    # ABA 2
    # =========================

    aba2 = driver.find_element(
        By.ID,
        "aba2-tab"
    )

    driver.execute_script(
        "arguments[0].click();",
        aba2
    )

    time.sleep(3)

    # =========================
    # MACRORREGIÕES
    # =========================

    macro = driver.find_element(
        By.XPATH,
        "//div[contains(., 'Macrorregiões')]"
    )

    driver.execute_script(
        "arguments[0].click();",
        macro
    )

    time.sleep(3)

    # =========================
    # BOTÃO EXPORTAR
    # =========================

    exportar = driver.find_element(
        By.ID,
        "exportar-dados-QV1-10"
    )

    # scroll até botão
    driver.execute_script(
        "arguments[0].scrollIntoView(true);",
        exportar
    )

    time.sleep(2)

    # clique JS (resolve overlay)
    driver.execute_script(
        "arguments[0].click();",
        exportar
    )

    print("Download iniciado...")

    time.sleep(15)

    driver.quit()

    # =========================
    # PEGA EXCEL BAIXADO
    # =========================

    arquivos = [
        f for f in os.listdir(PASTA_DOWNLOAD)
        if f.endswith(".xlsx")
    ]

    if not arquivos:
        raise Exception(
            "Nenhum Excel foi baixado."
        )

    arquivos.sort(
        key=lambda x: os.path.getmtime(
            os.path.join(PASTA_DOWNLOAD, x)
        )
    )

    ultimo = os.path.join(
        PASTA_DOWNLOAD,
        arquivos[-1]
    )

    # renomeia
    if ultimo != CAMINHO_EXCEL:

        if os.path.exists(CAMINHO_EXCEL):
            os.remove(CAMINHO_EXCEL)

        os.rename(
            ultimo,
            CAMINHO_EXCEL
        )

    print("Excel salvo com sucesso.")

def carregar_dados():
    """
    Carrega Excel em memória.
    """

    global df_global

    # cache simples
    if df_global is not None:
        return df_global

    # se não existir -> baixa
    if not os.path.exists(CAMINHO_EXCEL):
        baixar_excel()

    print("Lendo Excel...")

    df_global = pd.read_excel(CAMINHO_EXCEL)

    return df_global


def buscar_cobertura_estado(uf):
    """
    Consulta cobertura por estado.
    """

    df = carregar_dados()

    uf = uf.upper()

    df_filtrado = df[
        (df["UF Residência"] == uf)
        &
        (df["Macrorregião Saúde"] == "Totais")
    ]

    if df_filtrado.empty:
        return "Estado não encontrado."

    linha = df_filtrado.iloc[0]

    colunas_ignorar = [
        " ",
        "Região Ocorrência",
        "UF Residência",
        "Macrorregião Saúde",
        "Região de Saúde",
        "Município Residência",
        "Imunobiológico"
    ]

    resposta = f"📍 COBERTURA VACINAL — {uf}\n"
    resposta += "-" * 40 + "\n\n"

    valores = []

    for coluna in df.columns:

        if coluna not in colunas_ignorar:

            valor = linha[coluna]

            if pd.notna(valor) and valor != "-":

                percentual = round(float(valor) * 100, 2)

                valores.append(percentual)

                if percentual < 60:
                    emoji = "🔴"
                    status = "Crítico"

                elif percentual < 75:
                    emoji = "🟡"
                    status = "Atenção"

                else:
                    emoji = "🟢"
                    status = "Adequado"

                resposta += (
                    f"{emoji} {coluna}: "
                    f"{percentual}% ({status})\n"
                )

    media = round(sum(valores) / len(valores), 2)

    resposta += "\n"
    resposta += "-" * 40 + "\n"
    resposta += f"Média geral: {media}%"

    return resposta


def ranking_estados():
    """
    Ranking nacional.
    """

    df = carregar_dados()

    colunas_ignorar = [
        " ",
        "Região Ocorrência",
        "UF Residência",
        "Macrorregião Saúde",
        "Região de Saúde",
        "Município Residência",
        "Imunobiológico"
    ]

    df_totais = df[
        (df["UF Residência"].notna())
        &
        (df["Macrorregião Saúde"] == "Totais")
    ]

    resultado = []

    for _, linha in df_totais.iterrows():

        uf = linha["UF Residência"]

        valores = []

        for coluna in df.columns:

            if coluna not in colunas_ignorar:

                valor = linha[coluna]

                if pd.notna(valor) and valor != "-":

                    valores.append(
                        float(valor) * 100
                    )

        if valores:

            media = round(
                sum(valores) / len(valores),
                2
            )

            resultado.append((uf, media))

    resultado.sort(
        key=lambda x: x[1],
        reverse=True
    )

    resposta = "🇧🇷 RANKING DE COBERTURA\n\n"

    medalhas = {
        0: "🥇",
        1: "🥈",
        2: "🥉"
    }

    for i, (uf, media) in enumerate(resultado[:10]):

        medalha = medalhas.get(i, "📍")

        resposta += (
            f"{medalha} {uf} — {media}%\n"
        )

    return resposta

def normalizar(texto):

    texto = str(texto).lower().strip()

    texto = unicodedata.normalize(
        "NFD",
        texto
    )

    texto = "".join(
        c for c in texto
        if unicodedata.category(c) != "Mn"
    )

    return texto

def detectar_municipio(texto):

    df = carregar_dados()

    texto_norm = normalizar(texto)

    municipios = df[
        df["Município Residência"].notna()
    ]["Município Residência"].unique()

    for item in municipios:

        try:

            nome = item.split(" - ")[-1].strip()

            nome_norm = normalizar(nome)

            if nome_norm in texto_norm:
                return nome

        except:
            pass

    return None

def obter_estado_do_municipio(municipio):

    df = carregar_dados()

    municipio_norm = normalizar(municipio)

    df_mun = df[
        df["Município Residência"].notna()
    ]

    for _, linha in df_mun.iterrows():

        try:

            nome = linha[
                "Município Residência"
            ].split(" - ")[-1].strip()

            if normalizar(nome) == municipio_norm:

                return linha["UF Residência"]

        except:
            pass

    return None

def buscar_cobertura_municipio(
    estado,
    municipio
):

    df = carregar_dados()

    municipio_norm = normalizar(municipio)

    df_mun = df[

        (df["UF Residência"] == estado)
        &
        (df["Município Residência"].notna())

    ]

    mask = df_mun[
        "Município Residência"
    ].apply(

        lambda x:
        normalizar(
            x.split(" - ")[-1]
        ) == municipio_norm

    )

    df_filtrado = df_mun[mask]

    if df_filtrado.empty:
        return "Município não encontrado."

    linha = df_filtrado.iloc[0]

    colunas_ignorar = [
        " ",
        "Região Ocorrência",
        "UF Residência",
        "Macrorregião Saúde",
        "Região de Saúde",
        "Município Residência",
        "Imunobiológico"
    ]

    resposta = (
        f"📍 COBERTURA VACINAL — "
        f"{municipio}/{estado}\n"
    )

    resposta += "-" * 40 + "\n\n"

    valores = []

    for coluna in df.columns:

        if coluna not in colunas_ignorar:

            valor = linha[coluna]

            if (
                pd.notna(valor)
                and valor != "-"
            ):

                percentual = round(
                    float(valor) * 100,
                    2
                )

                valores.append(percentual)

                if percentual < 60:
                    emoji = "🔴"
                    status = "Crítico"

                elif percentual < 75:
                    emoji = "🟡"
                    status = "Atenção"

                else:
                    emoji = "🟢"
                    status = "Adequado"

                resposta += (
                    f"{emoji} {coluna}: "
                    f"{percentual}% "
                    f"({status})\n"
                )

    media = round(
        sum(valores) / len(valores),
        2
    )

    resposta += "\n"
    resposta += "-" * 40 + "\n"
    resposta += (
        f"Média geral: {media}%"
    )

    return resposta