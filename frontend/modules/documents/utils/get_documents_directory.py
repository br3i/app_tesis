import requests
import json

def get_documents_directory(BACKEND_URL):
    response = requests.get(f"{BACKEND_URL}/documents_directory")
    if response.status_code == 200:
        return response.json()  # Extrae solo los nombres de documentos
    return []