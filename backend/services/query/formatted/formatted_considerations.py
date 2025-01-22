import re


def formatted_considerations(data):
    replace_patterns = [
        (r"[\n\r\f]", " "),  # Reemplaza saltos de línea y de página por un espacio
        (r"\|", ","),  # Reemplaza "|" por una coma
        (r"\s{2,}", " "),  # Reemplaza múltiples espacios por uno solo
    ]

    def clean_text(text):
        for pattern, replacement in replace_patterns:
            text = re.sub(pattern, replacement, text)
        return text.strip()

    formatted_list = []
    for item in data:
        formatted_list.append(
            {
                "Documento": item.get("document_name", "Sin nombre"),
                "Consideraciones": clean_text(
                    item.get("considerations", "Sin consideraciones")
                ),
                "A quien se envió copia": item.get("copia", "Sin copia"),
            }
        )

    return " ".join(formatted_list)
