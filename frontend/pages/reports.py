import streamlit as st
from modules.menu.create_menu import create_menu

from modules.log_in.login import create_login
from modules.log_in.config_data.config_data import load_config, is_session_valid

BACKEND_URL = st.secrets.get('BACKEND_URL', 'Not found')

config = load_config()

# VERIFICAR LOGIN

print("[documents]")
# Crear el placeholder para mostrar mensajes de carga
placeholder = st.empty()

if 'username_logged' in st.session_state:
    create_menu(st.session_state['username'])
    st.title('Página :green[Reportes]')
    
    # Crear pestañas para las diferentes funcionalidades
    tabs = st.tabs(["Report1", "Report2", "Report3"])

    with tabs[0]:
        st.header(":green[Reporte1]")
        with st.spinner("Cargando..."):
            st.write(1)
    with tabs[1]:
        st.header(":green[Reporte2]")      
        with st.spinner("Cargando Reportes..."):
            st.write(2)
    with tabs[2]:
        st.header(":red[Reporte3]")
        with st.spinner("Cargando Reportes..."):
            st.write(3)

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
        st.title('Página :green[Reportes]')
    
        # Crear pestañas para las diferentes funcionalidades
        tabs = st.tabs(["Report1", "Report2", "Report3"])

        with tabs[0]:
            st.header(":green[Reporte1]")
            with st.spinner("Cargando..."):
                st.write(1)
        with tabs[1]:
            st.header(":green[Reporte2]")      
            with st.spinner("Cargando Reportes..."):
                st.write(2)
        with tabs[2]:
            st.header(":red[Reporte3]")
            with st.spinner("Cargando Reportes..."):
                st.write(3)
                
    else:
        st.info("Ingrese las credenciales para iniciar sesión.")
        placeholder = create_login()
