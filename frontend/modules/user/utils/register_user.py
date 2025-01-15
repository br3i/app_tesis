import streamlit as st
import json
import requests

BACKEND_URL = st.secrets.get('BACKEND_URL', 'Not found')
TIME_ZONE = st.secrets.get('TIME_ZONE', 'Not found')

def register_user(first_name_new, last_name_new, username_new, email_new, password_new, roles):
    print(f"[register_user] valores que llegan first_name_new : {first_name_new}, last_name_new : {last_name_new}, username_new : {username_new}, email_new : {email_new}, password_new : {password_new}, roles : {roles}, TIPO DE ROLES: {type(roles)}")
    try: 
        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "email": email_new,
            "username": username_new,
            "first_name": first_name_new,
            "last_name": last_name_new,
            "password": password_new,
            "roles": roles
        }

        print(f"[register_user] Se envía estos valores a create-user {payload}")
        response = requests.post(f"{BACKEND_URL}/create-user", json=payload, headers=headers)
        response_data = response.json()
        print("response_data: ", response_data)
        if response.status_code == 200:
            return response_data['username'], "success", "Usuario creado"
        return '', None, response_data['detail']
    except Exception as e:
        return '', None, e