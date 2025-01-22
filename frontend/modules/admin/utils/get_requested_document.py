import streamlit as st
import requests

BACKEND_URL = st.secrets.get('BACKEND_URL', 'Not found')

@st.cache_data(show_spinner=False, ttl=60)
def get_len_requested_document():
    response = requests.get(f"{BACKEND_URL}/requested_documents")
    print("[get_len_requested_document] response :", response.json())
    return len(response.json())

