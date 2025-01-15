import streamlit as st
import requests
from helpers.validator_fields import validate_email, validate_length, validate_name, validate_password, validate_username
from modules.user.utils.register_user import register_user

BACKEND_URL = st.secrets.get('BACKEND_URL', 'Not found')
MAX_FIRSTNAME_LENGTH = int(st.secrets.get('MAX_FIRSTNAME_LENGTH', 'Not found'))
MAX_LASTNAME_LENGTH = int(st.secrets.get('MAX_LASTNAME_LENGTH', 'Not found'))
MAX_USERNAME_LENGTH = int(st.secrets.get('MAX_USERNAME_LENGTH', 'Not found'))
MAX_PASSWORD_LENGTH = int(st.secrets.get('MAX_PASSWORD_LENGTH', 'Not found'))

def validate_register_user(first_name_new, last_name_new, username_new, email_new, password_new, repeat_password_new, roles):
    first_name_new = first_name_new.strip()
    last_name_new = last_name_new.strip()
    username_new = username_new.strip()
    email_new = email_new.strip()
    password_new = password_new.strip()
    repeat_password_new = repeat_password_new.strip()
    if not validate_name(first_name_new):
        return '', None, 'El primer nombre no es válido'
    if not validate_name(last_name_new):
        return '', None, 'El apellido no es válido'
    if not validate_username(username_new):
        return '', None, 'El nombre de usuario no es válido'
    if not validate_email(email_new):
        return '', None, 'El correo electrónico no es válido'
    if not validate_length(password_new, 1) \
        or not validate_length(repeat_password_new, 1):
        return '', None, 'Los campos de contraseña/repetir contraseña no pueden estar vacíos'
    if password_new != repeat_password_new:
        return '', None, 'Las contraseñas no coinciden'
    if not validate_password(password_new):
        return '', None, 'La contraseña no cumple con los criterios'

    return register_user(first_name_new, last_name_new, username_new, email_new, password_new, roles)

def show_form_register(roles):
    print("[show_form_register] Se ejecuta")
    frm_register_user = st.form('frm_register_user', clear_on_submit=False)
    # Título del formulario
    frm_register_user.subheader('Registro de usuario')

    col1, col2 = frm_register_user.columns([0.5, 0.5], gap="small", vertical_alignment="center")
    with col1:
        first_name_input = st.text_input('Primer nombre', max_chars=MAX_FIRSTNAME_LENGTH, help="Ingrese su primer nombre", placeholder="Ingrese su primer nombre", label_visibility="visible")

        last_name_input = st.text_input('Apellido', max_chars=MAX_LASTNAME_LENGTH, help="Ingrese su apellido", placeholder="Ingrese su primer apellido", label_visibility="visible")

    with col2:
        username_input = st.text_input('Usuario', max_chars=MAX_USERNAME_LENGTH, help="Ingrese un nombre de usuario", placeholder="Ingrese su nombre de usuario", label_visibility="visible")

        email_input = st.text_input('Email', help="""
            Ingresa una dirección de correo electrónico válida.\n
            Ejemplos:
            - usuario@gmail.com
            - nombre.apellido@outlook.com
            - contacto@empresa.com
        """, placeholder="usuario@correo.com", label_visibility="visible")
    
    col3, col4 = frm_register_user.columns([0.5, 0.5], gap="small", vertical_alignment="center")

    with col3:
        password_input = st.text_input('Contraseña', type="password", max_chars=MAX_PASSWORD_LENGTH, help="Ingrese una contraseña", placeholder="Ingrese su contraseña", label_visibility="visible")

    with col4:
        repeat_password_input = st.text_input('Repetir Contraseña', type="password", max_chars=MAX_PASSWORD_LENGTH, help="Repetir contraseña", placeholder="Repetir contraseña", label_visibility="visible")
        
    if frm_register_user.form_submit_button(label='Registrar', type="primary"):
        return validate_register_user(first_name_input, last_name_input, username_input, email_input, password_input, repeat_password_input, roles) 
    return None, False, None
    