import streamlit as st
import uuid
import pandas as pd
from modules.user.visuals.show_form_register import show_form_register
from modules.log_in.config_data.config_data import update_users_in_yaml
from modules.log_in.cache_data.load_data import load_users


def show_create_users():
    if "uu_key" not in st.session_state:
        st.session_state["uu_key"] = str(uuid.uuid4())

    with st.popover("Métodos"):
        on = st.radio(
            "Seleccione una opción",
            ["Formulario", ":orange[Subir archivo CSV]"],
            captions=[
                "Crear un usuario.",
                "Crear varios usuarios.",
            ],
        )

    if on == ":orange[Subir archivo CSV]":
        uploaded_files = st.file_uploader(
            "Elige un archivo",
            type=["csv"],
            accept_multiple_files=True,
            help="Seleccione los archivos",
            key=st.session_state.uu_key,
        )
        if uploaded_files:
            with st.spinner("Cargando..."):
                with st.expander("Documentos seleccionados"):
                    for uploaded_file in uploaded_files:
                        with st.container(border=True):
                            st.write(
                                f":material/upload_file: :orange[Nombre:] :violet[{uploaded_file.name}]"
                            )
                            st.write(
                                f":material/cloud_upload: :orange[Tamaño:] :violet[{uploaded_file.size / 1024:.2f} KB]"
                            )
        st.info(":material/info: Esta funcionalidad está en desarrollo")
    if on == "Formulario":
        # Creating a new user registration widget
        try:
            options_roles = ["user", "admin", "viewer"]
            # Diccionario de traducción a español con la primera letra en mayúscula
            roles_translation = {
                "user": "Usuario",
                "admin": "Administrador",
                "viewer": "Espectador",
            }

            translated_roles = [roles_translation[role] for role in options_roles]
            with st.container(border=True):
                selection_roles = st.pills(
                    "**Roles**",
                    translated_roles,
                    selection_mode="multi",
                    default=["Usuario"],
                )
            placeholder_info = st.empty()
            selected_roles_in_english = [
                options_roles[translated_roles.index(role)] for role in selection_roles
            ]
            # st.markdown(f"Your selected options: {selected_roles_in_english}.")

            if selected_roles_in_english:
                print(
                    "Tipo de selected_roles_in_english: ",
                    type(selected_roles_in_english),
                )
                username_new, status_register, message = show_form_register(
                    selected_roles_in_english
                )
                if status_register == "success":
                    placeholder_info.success(
                        f"{message}: {username_new}", icon=":material/check:"
                    )
                    load_users.clear()
                    update_users_in_yaml()
                    del st.session_state.users_df
                    del st.session_state.selected_user
                    del st.session_state.selected_roles
                    del st.session_state.df_u_key
                    del st.session_state.original_roles_df

                    # Recargar los usuarios y actualizar la tabla
                    load_users.clear()
                    users = load_users()
                    users_data = []
                    if users:
                        for user in users:
                            users_data.append(
                                {
                                    "id": user["id"],
                                    "email": user["email"],
                                    "username": user["username"],
                                    "first_name": user["first_name"],
                                    "last_name": user["last_name"],
                                    "roles": user["roles"],
                                }
                            )

                    # Convertir la lista de usuarios a un DataFrame
                    users_df = pd.DataFrame(users_data)

                    # Actualizar session_state con los nuevos datos
                    st.session_state.users_df = users_df
                    st.session_state["df_u_key"] = str(uuid.uuid4())
                    st.session_state["original_roles_df"] = users_df.copy()

                    st.rerun()
                if status_register is None:
                    placeholder_info.error(message, icon=":material/gpp_maybe:")
            else:
                placeholder_info = st.error(
                    "Por favor seleccione al menos un Rol", icon=":material/gpp_maybe:"
                )
        except Exception as e:
            placeholder_info.error(e)
