import re

def extract_resolution_info(query: str):
    # Expresión regular para buscar años o números de resolución
    year_pattern = r'\b(\d{4})\b'  # Busca un año (4 dígitos)
    resolution_pattern = r'\b(\d+)\b'  # Busca cualquier número

    # Buscar año y número de resolución en la pregunta
    years = re.findall(year_pattern, query)
    resolutions = re.findall(resolution_pattern, query)

    # Si encuentras un año, puedes tomarlo como el año de interés
    year = years[-1] if years else None  # Tomar el último año encontrado
    resolution = resolutions[-1] if resolutions else None  # Tomar el último número de resolución

    if resolution:
        resolution = resolution.zfill(3)
        
    return year, resolution
