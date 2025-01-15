# headers = {
#     "Content-Type": "application/json"
# }

# payload = {
#     "code": f"{code}",
#     "user_id": f"{st.session_state['user_id']}"
# }

# response = requests.post(f"{BACKEND_URL}/create-code", json=payload, headers=headers)

import streamlit as st
import requests
import json

BACKEND_URL = st.secrets.get('BACKEND_URL', 'Not found')

@st.cache_data(show_spinner=False, ttl=60)
def notifications_created():
    response = requests.get(f"{BACKEND_URL}/notifications")
    # Si la respuesta fue exitosa, devuelve los datos JSON de las notificaciones
    if response.status_code == 200:
        return response.json()  # Retorna la respuesta como JSON
    else:
        st.error("Error al obtener las notificaciones.")
        return []