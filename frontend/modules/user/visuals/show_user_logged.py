import streamlit as st
from modules.user.visuals.show_create_users import show_create_users
from modules.user.visuals.show_df_users import show_df_users
from modules.user.visuals.show_df_dlt_users import show_df_dlt_users
from modules.settings.utils.load_theme_extra_config import load_theme_extra_config

theme_extra_config = load_theme_extra_config()

def show_user_logged():
    # Crear pestañas para las diferentes funcionalidades
    tabs = st.tabs(["Crear Usuarios", "Editar Usuarios", "Eliminar Usuarios"])

    with tabs[0]:
        st.header(f':{theme_extra_config["secondary_users_color"]}[Crear Usuarios]')
        with st.spinner("Cargando..."):
            show_create_users()
    with tabs[1]:
        st.header(f':{theme_extra_config["secondary_users_color"]}[Usuarios Disponibles]')
        with st.spinner("Cargando..."):
            show_df_users()
    with tabs[2]:
        st.header(f':{theme_extra_config["secondary_users_color"]}[Usuarios Disponibles]')
        with st.spinner("Cargando..."):
            show_df_dlt_users()