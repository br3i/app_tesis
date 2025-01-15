import streamlit as st
import requests

BACKEND_URL = st.secrets.get('BACKEND_URL', 'Not found')

@st.cache_data(show_spinner=False, ttl=60)
def active_users():
    response = requests.get(f"{BACKEND_URL}/users")
    # retornar la cantidad de usuarios existentes
    return len(response.json())

