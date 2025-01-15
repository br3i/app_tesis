import streamlit as st
import requests
import json

BACKEND_URL = st.secrets.get("BACKEND_URL", "Not found")

@st.cache_data(show_spinner=False, ttl=60)
def get_collections():
    response = requests.get(f"{BACKEND_URL}/collection_names")
    if response.status_code == 200:
        return response.json().get("collections", [])
    return []