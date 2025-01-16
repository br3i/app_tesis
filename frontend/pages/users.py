import streamlit as st
from modules.menu.create_menu import create_menu
from modules.user.visuals.show_user_logged import show_user_logged
from modules.log_in.login import create_login
from modules.log_in.config_data.config_data import load_config, is_session_valid
from modules.settings.utils.load_theme_extra_config import load_theme_extra_config

# Configuración inicial
BACKEND_URL = st.secrets.get("BACKEND_URL", "Not found")

config = load_config()
theme_extra_config = load_theme_extra_config()

# Crear el placeholder para mostrar mensajes de carga
placeholder = st.empty()

if 'username_logged' in st.session_state:
    create_menu(st.session_state['username'])
    st.title(f'Administración de :{theme_extra_config["primary_users_color"]}[Usuarios :material/group:]')
    
    show_user_logged()
else:
    username_logged = None
    for username, user_data in config['credentials']['usernames'].items():
        if user_data['logged_in'] and is_session_valid(username):
            username_logged = username
            break
    
    if username_logged:
        # Restaurar sesión en `st.session_state`
        st.session_state['username_logged'] = True
        st.session_state['username'] = username_logged

        create_menu(st.session_state['username'])
        st.title(f'Administración de :{theme_extra_config["primary_users_color"]}[Usuarios :material/group:]')
        
        show_user_logged()  

    else:
        st.info("Ingrese las credenciales para iniciar sesión.")
        placeholder= create_login()
