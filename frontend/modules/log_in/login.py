import streamlit as st
import pandas as pd
import requests
import bcrypt
import pytz
from datetime import datetime
from helpers.show_toast import show_toast
from modules.admin.dialogs.forgot_password_dialog import forgot_password_dialog
from modules.admin.dialogs.verify_code_dialog import verify_code_dialog
from modules.admin.dialogs.new_password_dialog import new_password_dialog
from modules.admin.dialogs.forgot_username_dialog import forgot_username_dialog
from modules.log_in.cache_data.load_data import load_users, load_user
from modules.log_in.config_data.config_data import load_config, save_config

BACKEND_URL = st.secrets.get('BACKEND_URL', "Not Found")
NOMBRE_ASISTENTE = st.secrets.get('NOMBRE_ASISTENTE', "Not Found")
TIME_ZONE = st.secrets.get("TIME_ZONE", "Not Found")

tz = pytz.timezone(TIME_ZONE)

def validate_user(username, password):
    try:
        response = load_user(username)
        
        if response:
            hashed_password = response["password"]

            if bcrypt.checkpw(password.encode(), hashed_password.encode()):
                return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error al validar usuario: {e}")
        return False

    return False

def create_login():
    if st.session_state.get("password_changed") is True:
        show_toast("¡Contraseña cambiada exitosamente!", icon="✔")
        st.session_state["password_changed"] = None
        st.session_state["username_user"] = None
        st.session_state["user_id"] = None
    elif st.session_state.get("password_changed") is False:
        show_toast("No se pudo cambiar la contraseña. Verifica los datos e inténtalo de nuevo.", icon="❌")
        st.session_state["password_changed"] = None

    if st.session_state.get("username_sent") is True:
        st.session_state["username_sent"] = False

    if st.session_state.get("email_recovery_sent") is True:
        st.session_state["email_recovery_sent"] = False

    if st.session_state.get("code_sent") is True:
        st.session_state["code_sent"] = None
        verify_code_dialog()
    
    if st.session_state.get("code_right") is True:
        st.session_state["code_right"] = None
        new_password_dialog()



    with st.container():
        with st.form('frm_login', clear_on_submit=False):
            # Título del formulario
            st.subheader('Inicio de Sesión')
            
            # Campos del formulario
            username_input = st.text_input('Usuario', placeholder="Ingrese su nombre de usuario")
            password_input = st.text_input('Contraseña', type='password', placeholder="Ingrese su contraseña")
            
            # Botón de envío
            btn_login = st.form_submit_button('Ingresar', type='primary')

            # Validación de credenciales
            if btn_login:
                if validate_user(username_input, password_input):
                    st.session_state['username'] = username_input
                    st.session_state['username_logged'] = True
                    # Registrar el último login
                    config = load_config()
                    current_time = datetime.now(tz)
                    config['credentials']['usernames'][username_input]['logged_in'] = True
                    config['credentials']['usernames'][username_input]['last_login'] = current_time.isoformat()
                    save_config(config)
                    st.rerun()
                else:
                    st.error("Usuario o clave inválidos",icon=":material/gpp_maybe:")
        col1, col2 = st.columns([1, 2], gap="small", vertical_alignment="center")
        with col1:
            if st.button("Olvidó la contraseña?"):
                forgot_password_dialog()
        with col2:
            if st.button("Olvidó el nombre de usuario?"):
                forgot_username_dialog()            