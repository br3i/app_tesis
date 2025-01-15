import streamlit as st
import requests
import json

BACKEND_URL = st.secrets.get("BACKEND_URL", "Not found")

@st.cache_data(show_spinner=False, ttl=200)
def get_documents_from_db():
    response = requests.get(f"{BACKEND_URL}/documents_from_db")
    if response.status_code == 200:
        return response.json()
    return []

@st.cache_data(show_spinner=False, ttl=60)
def get_len_documents_from_db():
    try:
        response = requests.get(f"{BACKEND_URL}/documents_from_db")
        # Verificar si la respuesta es exitosa
        response.raise_for_status()  # Lanza un error si el código de estado no es 2xx
        data = response.json()
        
        # Verificar que la respuesta sea una lista
        if isinstance(data, list):
            return len(data)
        else:
            st.warning("La respuesta de la API no es una lista.")
            return 0
    except requests.exceptions.RequestException as e:
        # Manejo de errores si la solicitud falla
        st.error(f"Error al obtener los documentos: {e}")
        return 0

