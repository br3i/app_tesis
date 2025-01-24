import streamlit as st
from modules.log_in.cache_data.load_data import load_user
from modules.log_in.config_data.config_data import handle_logout
from modules.settings.utils.load_theme_extra_config import load_theme_extra_config

theme_extra_config = load_theme_extra_config()

NOMBRE_ASISTENTE = st.secrets.get("NOMBRE_ASISTENTE", "Not found")


def create_menu(username):
    with st.sidebar:
        user_data = load_user(username)
        if user_data:
            full_name = user_data["first_name"] + " " + user_data["last_name"]

            st.write(
                f"Hola **:{theme_extra_config['menu_name_color']}-background[{full_name.title()}]** "
            )

            st.page_link("pages/admin.py", label="Inicio", icon=":material/home:")
            st.page_link(
                "pages/profile.py", label="Perfil", icon=":material/account_box:"
            )
            st.page_link(
                "pages/assistant.py",
                label=f"{NOMBRE_ASISTENTE}",
                icon=":material/robot_2:",
            )
            st.page_link(
                "pages/documents.py", label="Archivos", icon=":material/folder_open:"
            )
            st.page_link(
                "pages/reports.py", label="Reportes", icon=":material/bar_chart:"
            )
            st.page_link(
                "pages/metrics.py", label="Métricas", icon=":material/timeline:"
            )
            st.page_link("pages/users.py", label="Usuarios", icon=":material/group:")
            st.page_link(
                "pages/audit.py", label="Auditoría", icon=":material/security:"
            )
            st.page_link(
                "pages/settings.py", label="Configuración", icon=":material/settings:"
            )
            st.page_link("pages/help.py", label="Documentación", icon=":material/help:")
            btn_logout = st.button("Salir")
            if btn_logout:
                handle_logout()
        else:
            st.error("Usuario no encontrado. Por favor, revise sus credenciales.")
