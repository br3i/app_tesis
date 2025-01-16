import streamlit as st
from modules.menu.create_menu import create_menu
from modules.documents.visuals.show_upload_docs import show_upload_docs
from modules.documents.visuals.show_df_documents import show_df_documents
from modules.documents.visuals.show_df_delete import show_df_delete
from modules.log_in.login import create_login
from modules.log_in.config_data.config_data import load_config, is_session_valid
from modules.settings.utils.load_theme_extra_config import load_theme_extra_config

BACKEND_URL = st.secrets.get('BACKEND_URL', 'Not found')

config = load_config()
theme_extra_config = load_theme_extra_config()

# Crear el placeholder para mostrar mensajes de carga
placeholder = st.empty()

if 'username_logged' in st.session_state:
    create_menu(st.session_state['username'])
    st.title(f'Página :{theme_extra_config["primary_docs_color"]}[Gestión de Archivos]')
    
    # Crear pestañas para las diferentes funcionalidades
    tabs = st.tabs(["Subir Archivo", "Editar Archivos", "Eliminar Archivos"])

    with tabs[0]:
        st.header(f':{theme_extra_config["secondary_docs_color"]}[Subir un PDF]')
        with st.spinner("Cargando..."):
            show_upload_docs()
    with tabs[1]:
        st.header(f':{theme_extra_config["secondary_docs_color"]}[Archivos Disponibles]')
        with st.spinner("Cargando Archivos..."):
            show_df_documents()
    with tabs[2]:
        st.header(':red[Archivos Disponibles]')
        with st.spinner("Cargando Archivos..."):
            show_df_delete()

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
        st.title(f'Página :{theme_extra_config["primary_docs_color"]}[Gestión de Archivos]')
    
        # Crear pestañas para las diferentes funcionalidades
        tabs = st.tabs(["Subir Archivo", "Editar Archivos", "Eliminar Archivos"])

        with tabs[0]:
            st.header(f':{theme_extra_config["secondary_docs_color"]}[Subir un PDF]')
            with st.spinner("Cargando..."):
                show_upload_docs()
        with tabs[1]:
            st.header(f':{theme_extra_config["secondary_docs_color"]}[Archivos Disponibles]')
            with st.spinner("Cargando Archivos..."):
                show_df_documents()
        with tabs[2]:
            st.header(':red[Archivos Disponibles]')
            with st.spinner("Cargando Archivos..."):
                show_df_delete()
    else:
        st.info("Ingrese las credenciales para iniciar sesión.")
        placeholder = create_login()