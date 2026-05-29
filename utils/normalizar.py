# utils/normalizar.py

import unicodedata


def normalizar(texto: str) -> str:
    """Remove acentos, converte para minúsculas e elimina espaços extras."""
    texto = str(texto).lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(
        c for c in texto
        if unicodedata.category(c) != "Mn"
    )
    return texto