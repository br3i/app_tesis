import streamlit as st
import requests

BACKEND_URL = st.secrets.get('BACKEND_URL', 'Not found')

@st.cache_data(show_spinner=False, ttl=700)
def get_roles():
    response = requests.get(f"{BACKEND_URL}/user_roles")
    if response.status_code == 200:
        return response.json()
    return None
