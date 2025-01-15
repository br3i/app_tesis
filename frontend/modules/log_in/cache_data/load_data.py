import streamlit as st
import requests

BACKEND_URL = st.secrets.get("BACKEND_URL", "Not found")

@st.cache_data(show_spinner=False, ttl=120)
def load_users():
    print("[load_users]")
    response = requests.get(f"{BACKEND_URL}/users")
    if response.status_code == 200:
        return response.json()
    return None

@st.cache_data(show_spinner=False, ttl=120)
def load_user(username):
    response = requests.get(f"{BACKEND_URL}/user/username/{username}")

    if response.status_code == 200:
        return response.json()
    return None
