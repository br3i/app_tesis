import streamlit as st
import requests
import bcrypt

BACKEND_URL = st.secrets.get("BACKEND_URL", "Not found")

def change_password(user_id: int, password: str):
    headers = {
        "Content-Type": "application/json"
    }

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    payload = {
        "password": hashed_password
    }

    try:
        # Hacer la solicitud PUT al backend
        print('[chang_pass] tipo de user_id: ', type(user_id))
        print('[chang_pass] user_id: ', user_id)

        response = requests.put(f"{BACKEND_URL}/change-password/{user_id}", json=payload, headers=headers)

        # Verificar el estado de la respuesta
        if response.status_code == 200:
            data = response.json()
            print(data.get("message", "Contraseña actualizada exitosamente"))
            st.cache_data.clear()
            return True 
        elif response.status_code == 404:
            data = response.json()
            print(data.get("detail", "Usuario no encontrado"))
            return False
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
        return None