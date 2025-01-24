import streamlit as st
from modules.admin.visuals.show_main_dashboard import show_main_dashboard
from modules.menu.create_menu import create_menu
from modules.log_in.login import create_login
from modules.log_in.config_data.config_data import load_config, is_session_valid

config = load_config()

# with st.status("Valores en st.session_state"):
#     for key in st.session_state:
#         st.markdown(f"**Key**: `{key}`  \n**Value**: `{st.session_state[key]}`")

placeholder = st.empty()

if "username_logged" in st.session_state:
    create_menu(st.session_state["username"])
    show_main_dashboard()
else:
    print("[recargo la pagina]")
    username_logged = None
    for username, user_data in config["credentials"]["usernames"].items():
        print(f"[ciclo for] username: {username} - user_data: {user_data}")
        if user_data["logged_in"] and is_session_valid(username):
            print(f"[1 condicional]")
            username_logged = username
            print(f"[username_logged] {username_logged}")
            break

    if username_logged:
        print(f"[2 condicional]")
        # Restaurar sesión en `st.session_state`
        st.session_state["username_logged"] = True
        st.session_state["username"] = username_logged
        print(f"[st.ss.username_logged] {st.session_state['username_logged']}")
        show_main_dashboard()
        create_menu(username_logged)
        with placeholder:
            st.status("Valores en st.session_state")
            for key in st.session_state:
                st.markdown(f"**Key**: `{key}`  \n**Value**: `{st.session_state[key]}`")
    else:
        # Redirigir al login si no hay sesión activa
        st.info("Ingrese las credenciales para iniciar sesión.")
        # Crear el login
        placeholder = create_login()


# show_credentials(config)
