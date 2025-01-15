import streamlit as st
from modules.user.visuals.show_create_users import show_create_users
from modules.user.visuals.show_df_users import show_df_users
from modules.user.visuals.show_df_dlt_users import show_df_dlt_users

def show_user_logged():
    # Crear pestañas para las diferentes funcionalidades
    tabs = st.tabs(["Crear Usuarios", "Editar Usuarios", "Eliminar Usuarios"])

    with tabs[0]:
        st.header(":violet[Crear Usuarios]")
        with st.spinner("Cargando..."):
            show_create_users()
    with tabs[1]:
        st.header(":violet[Usuarios Disponibles]")
        with st.spinner("Cargando..."):
            show_df_users()
    with tabs[2]:
        st.header(":red[Usuarios Disponibles]")
        with st.spinner("Cargando..."):
            show_df_dlt_users()