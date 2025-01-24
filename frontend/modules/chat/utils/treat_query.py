import re
import unicodedata


def treat_query(query):
    treated_query = query.lower()

    treated_query = treated_query.replace("ñ", "\001")

    treated_query = "".join(
        c
        for c in unicodedata.normalize("NFD", treated_query)
        if unicodedata.category(c) != "Mn"
    )

    treated_query = treated_query.replace("\001", "ñ")

    # Lista de patrones y sus reemplazos
    replacements = [
        (r"[^a-z0-9áéíóúüñ%.,:=()/\- ]", ""),  # Eliminar caracteres no permitidos
        (r"\.\s*-\s*", "."),  # Reemplazar .- o . - por .
        (r"-{2,}", "-"),  # Reducir guiones consecutivos a uno solo
        (r"\.{2,}", "."),  # Reducir puntos consecutivos a uno solo
        (r"\(\.\)", ""),  # Eliminar el punto y los paréntesis (.)
        (r"/{2,}", "/"),  # Reducir barras consecutivas a una sola
        (r"\s{2,}", " "),  # Reducir espacios múltiples a uno solo
        (r";", ","),  # Reemplazar ; por ,
    ]

    # Aplicar cada reemplazo al texto
    for pattern, replacement in replacements:
        treated_query = re.sub(pattern, replacement, treated_query)

    return treated_query
