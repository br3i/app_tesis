import streamlit as st
import json
import requests
import uuid
import numpy as np
import pandas as pd
import time
from modules.user.decorators.get_roles import get_roles
from modules.user.utils.reset_df_dlt_user import reset_df_dlt_user
from modules.log_in.config_data.config_data import sync_deleted_users
from modules.log_in.cache_data.load_data import load_users
from helpers.show_toast import show_toast

BACKEND_URL = st.secrets.get("BACKEND_URL", "Not found")
MAX_FIRSTNAME_LENGTH = int(st.secrets.get("MAX_FIRSTNAME_LENGTH", "Not found"))
MAX_LASTNAME_LENGTH = int(st.secrets.get("MAX_LASTNAME_LENGTH", "Not found"))
MAX_USERNAME_LENGTH = int(st.secrets.get("MAX_USERNAME_LENGTH", "Not found"))


def show_df_dlt_users():
    # Obtener datos de usuarios y roles
    users = load_users()
    roles = get_roles()
    placeholder_success = st.empty()
    placeholder_warning = st.empty()
    placeholder_error = st.empty()

    placeholder_error.error(
        ":material/gpp_maybe: Asegurese de seleccionar solo los usuarios que desea eliminar."
    )

    if users:
        users_data = []
        for user in users:
            users_data.append(
                {
                    "id": user["id"],
                    "email": user["email"],
                    "username": user["username"],
                    "first_name": user["first_name"],
                    "last_name": user["last_name"],
                    "roles": user["roles"],
                    "Eliminar": False,
                }
            )

        # Convertir la lista de usuarios a un DataFrame
        users_df = pd.DataFrame(users_data)

        if "df_u_dlt_key" not in st.session_state:
            st.session_state["df_u_dlt_key"] = str(uuid.uuid4())

        # Mostrar los datos en un data_editor editable
        with st.spinner("Cargando usuarios..."):
            selected_df = st.data_editor(
                users_df.drop(columns=["id"]),
                column_config={
                    "Eliminar": st.column_config.CheckboxColumn(
                        "Eliminar",
                        help="Seleccione para eliminar",
                        default=False,
                        pinned=True,
                    ),
                    "username": st.column_config.TextColumn(
                        "Usuario",
                        disabled=True,
                        width="small",
                        max_chars=MAX_USERNAME_LENGTH,
                    ),
                    "email": st.column_config.TextColumn(
                        "Email", disabled=True, width="small"
                    ),
                    "first_name": st.column_config.TextColumn(
                        "Primer Nombre", disabled=True, width="small"
                    ),
                    "last_name": st.column_config.TextColumn(
                        "Apellido", disabled=True, width="small"
                    ),
                    "roles": st.column_config.ListColumn(
                        label="Rol", width="small", help="Rol asigando al usuario"
                    ),
                },
                hide_index=True,
                use_container_width=True,
                num_rows="fixed",
                key=st.session_state.df_u_dlt_key,
            )

        # Filtrar los usuarios seleccionados para eliminar
        rows_to_delete = []
        for index, row in selected_df.iterrows():
            if row["Eliminar"]:
                user_id = users_df.iloc[index]["id"]  # type: ignore
                rows_to_delete.append(
                    {
                        "index": index,
                        "user_id": user_id,
                    }
                )

        # Columna para los botones de acción
        cols = st.columns([1, 1, 10], gap="small")
        with cols[0]:
            if st.button(":material/delete:", type="primary", use_container_width=True):
                if rows_to_delete:
                    with st.spinner("Eliminando usuarios..."):
                        for row in rows_to_delete:
                            user_id = row["user_id"]
                            response = requests.delete(
                                f"{BACKEND_URL}/delete_user/{user_id}"
                            )
                            if response.status_code == 200:
                                placeholder_success.success(
                                    f":material/check: Usuario '{users[row['index']]['username']}' eliminado correctamente!"
                                )
                                sync_deleted_users()
                            else:
                                st.error(
                                    f":material/gpp_maybe: Error al eliminar el usuario '{users[row['index']]['username']}'."
                                )
                    load_users.clear()
                    users = load_users()
                    st.rerun()
                else:
                    placeholder_warning.warning(
                        "⚠️ No se detectaron usuarios seleccionados para eliminar."
                    )
        with cols[1]:
            st.button(
                ":material/refresh:",
                on_click=reset_df_dlt_user,
                use_container_width=True,
                key="btn_refres_dlt_user",
            )
    else:
        placeholder_warning.warning("⚠️ No hay usuarios disponibles en este momento.")
