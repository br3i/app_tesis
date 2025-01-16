import streamlit as st
from modules.menu.create_menu import create_menu
from modules.settings.utils.load_theme_config import load_theme_config
from modules.settings.utils.load_theme_extra_config import load_theme_extra_config
from modules.settings.visuals.change_theme_config import change_theme_config
from modules.log_in.login import create_login
from modules.log_in.config_data.config_data import load_config, is_session_valid

BACKEND_URL = st.secrets.get('BACKEND_URL', 'Not found')

config = load_config()
theme_config = load_theme_config()
theme_extra_config = load_theme_extra_config()

# Crear el placeholder para mostrar mensajes de carga
placeholder = st.empty()

if "switch_theme" not in st.session_state:
    if theme_config["backgroundColor"] == "#FFFFFF":
        st.session_state.switch_theme = "dark"
    else:
        st.session_state.switch_theme = "light"

if 'saved_changed_theme' not in st.session_state:
    st.session_state.saved_changed_theme = False

def saved_changed_theme():
    st.session_state.saved_changed_theme = True
    st.session_state.saved_changed_theme

if 'username_logged' in st.session_state:
    create_menu(st.session_state['username'])
    st.title(f'Configuración :{theme_extra_config["primary_config_color"]}[Global]')
    with st.spinner("Cargando..."):
        change_theme_config(theme_config, theme_extra_config)
            
else:
    print("[recargo la pagina]")
    username_logged = None
    for username, user_data in config['credentials']['usernames'].items():
        print(f"[ciclo for] username: {username} - user_data: {user_data}")
        if user_data['logged_in'] and is_session_valid(username):
            print(f"[1 condicional]")
            username_logged = username
            print(f"[username_logged] {username_logged}")
            break
    
    if username_logged:
        print(f"[2 condicional]")
        # Restaurar sesión en `st.session_state`
        st.session_state['username_logged'] = True
        st.session_state['username'] = username_logged
        print(f"[st.ss.username_logged] {st.session_state['username_logged']}")

        create_menu(username_logged)
        st.title(f'Configuración :{theme_extra_config["primary_config_color"]}[Global]')
        with st.spinner("Cargando..."):
            change_theme_config(theme_config, theme_extra_config)
    else:
        st.info("Ingrese las credenciales para iniciar sesión.")
        placeholder = create_login()