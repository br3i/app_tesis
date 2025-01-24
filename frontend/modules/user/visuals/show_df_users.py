import streamlit as st
import json
import requests
import uuid
import numpy as np
import pandas as pd
import time
from modules.user.decorators.get_roles import get_roles
from modules.user.utils.reset_df_user import reset_df_user
from modules.log_in.config_data.config_data import update_users_in_yaml
from modules.log_in.cache_data.load_data import load_users
from helpers.show_toast import show_toast

BACKEND_URL = st.secrets.get("BACKEND_URL", "Not found")
MAX_FIRSTNAME_LENGTH = int(st.secrets.get("MAX_FIRSTNAME_LENGTH", "Not found"))
MAX_LASTNAME_LENGTH = int(st.secrets.get("MAX_LASTNAME_LENGTH", "Not found"))
MAX_USERNAME_LENGTH = int(st.secrets.get("MAX_USERNAME_LENGTH", "Not found"))


def convert_int64_to_int(value):
    if isinstance(value, np.integer):
        return int(value)
    elif isinstance(value, pd.Timestamp):
        return value.value
    return value


def nan_to_none(value):
    if isinstance(value, float) and np.isnan(value):
        return None
    return value


def procesar_cambios(idx, differences_roles, differences, edited_df, original_df):
    id_usuario = original_df.loc[idx, "id"]
    cambios = {}

    # Procesar cambios en roles si existen
    if not differences_roles.empty and idx in differences_roles.index:
        cambios_fila_roles = differences_roles.loc[idx]
        cambios["roles"] = {
            "after": nan_to_none(
                cambios_fila_roles.get(("roles", "self"), edited_df.loc[idx, "roles"])
            ),
            "before": nan_to_none(
                cambios_fila_roles.get(
                    ("roles", "other"), original_df.loc[idx, "roles"]
                )
            ),
        }

    # Procesar cambios en otros campos si existen
    if not differences.empty and idx in differences.index:
        cambios_fila_otros = differences.loc[idx]
        for col in differences.columns.get_level_values(0).unique():
            cambios[col] = {
                "after": nan_to_none(
                    cambios_fila_otros.get((col, "self"), edited_df.loc[idx, col])
                ),
                "before": nan_to_none(
                    cambios_fila_otros.get((col, "other"), original_df.loc[idx, col])
                ),
            }

    return id_usuario, cambios


def show_df_users():
    # Obtener datos de usuarios y roles
    users = load_users()
    roles = get_roles()
    options_roles = roles["roles"] if roles else []

    placeholder_info = st.empty()
    placeholder_success = st.empty()
    placeholder_warning = st.empty()
    placeholder_error = st.empty()

    placeholder_info.info(
        ":material/info: Si desea editar roles, hagalo primero y actualice la tabla."
    )

    if users:
        users_data = []
        for user in users or []:
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

        if "users_df" not in st.session_state:
            st.session_state.users_df = users_df.copy()
        if "selected_user" not in st.session_state:
            st.session_state.selected_user = None
        if "selected_roles" not in st.session_state:
            st.session_state.selected_roles = []
        if "df_u_key" not in st.session_state:
            st.session_state["df_u_key"] = str(uuid.uuid4())
        if "original_roles_df" not in st.session_state:
            st.session_state["original_roles_df"] = st.session_state["users_df"].copy()

        original_df = st.session_state.users_df.copy()

        st.session_state.users_df["roles"] = st.session_state.users_df["roles"].apply(
            lambda x: (
                x
                if isinstance(x, list)
                else (x.split(", ") if isinstance(x, str) else [])
            )
        )

        # Sección de edición de roles
        with st.expander("Edición de Roles"):
            col1, col2 = st.columns(
                [0.3, 0.7], gap="small", vertical_alignment="center"
            )

            with col1:
                selected_user = st.selectbox(
                    "Seleccione un usuario",
                    options=st.session_state.users_df["username"].tolist(),
                    index=(
                        0
                        if st.session_state.selected_user is None
                        else st.session_state.users_df[
                            st.session_state.users_df["username"]
                            == st.session_state.selected_user
                        ].index[0]
                    ),
                    key="user_selector",
                )

                user_roles = st.session_state.users_df[
                    st.session_state.users_df["username"] == selected_user
                ]["roles"].iloc[0]

                st.session_state.selected_roles = (
                    user_roles
                    if isinstance(user_roles, list)
                    else user_roles.split(", ")
                )

            with col2:
                updated_roles = st.multiselect(
                    "Seleccione los roles para el usuario",
                    options=options_roles,
                    default=st.session_state.selected_roles,
                    key="roles_editor",
                )

            if st.button("Actualizar Tabla", type="primary"):
                st.session_state.users_df.loc[
                    st.session_state.users_df["username"] == selected_user, "roles"
                ] = ", ".join(updated_roles)

                placeholder_success.success(
                    f":material/check: Roles del usuario '{selected_user}' actualizados correctamente."
                )
                st.session_state.selected_roles = updated_roles
                st.session_state.users_df = st.session_state.users_df.copy()

        st.session_state.users_df["roles"] = st.session_state.users_df["roles"].apply(
            lambda x: (
                x
                if isinstance(x, list)
                else (x.split(", ") if isinstance(x, str) else [])
            )
        )

        # Mostrar los datos en un data_editor editable
        edited_df = st.data_editor(
            st.session_state.users_df,
            column_config={
                "id": st.column_config.NumberColumn("ID", disabled=True, pinned=True),
                "username": st.column_config.TextColumn(
                    "Usuario",
                    required=True,
                    width="small",
                    max_chars=MAX_USERNAME_LENGTH,
                ),
                "email": st.column_config.TextColumn(
                    "Email", required=True, width="small"
                ),
                "first_name": st.column_config.TextColumn(
                    "Primer Nombre",
                    required=True,
                    width="small",
                    max_chars=MAX_FIRSTNAME_LENGTH,
                ),
                "last_name": st.column_config.TextColumn(
                    "Apellido",
                    required=True,
                    width="small",
                    max_chars=MAX_LASTNAME_LENGTH,
                ),
                "roles": st.column_config.ListColumn(
                    label="Rol",
                    width="small",
                    help="Rol asigando al usuario",
                ),
            },
            hide_index=True,
            use_container_width=True,
            num_rows="fixed",
            key=st.session_state.df_u_key,
        )

        cols = st.columns([1, 1, 10], gap="small")
        with cols[0]:
            # Botón para guardar cambios
            if st.button(":material/save:", type="primary", use_container_width=True):
                # Comparar los DataFrames para identificar diferencias
                differences_roles = edited_df.compare(
                    st.session_state["original_roles_df"]
                )
                differences = edited_df.compare(original_df)

                # Verificar si hay cambios en roles o en otros campos
                if not differences_roles.empty or not differences.empty:
                    placeholder_info.info(
                        ":material/info: Se encontraron diferencias entre los datos editados y los originales. Actualizando..."
                    )

                    for idx in set(differences_roles.index).union(differences.index):
                        id_usuario, cambios = procesar_cambios(
                            idx, differences_roles, differences, edited_df, original_df
                        )

                        # Construir el JSON para la solicitud
                        data = {
                            "id": convert_int64_to_int(id_usuario),
                            "email": nan_to_none(
                                cambios.get("email", {}).get(
                                    "after", original_df.loc[idx, "email"]
                                )
                            )
                            or original_df.loc[idx, "email"],
                            "username": nan_to_none(
                                cambios.get("username", {}).get(
                                    "after", original_df.loc[idx, "username"]
                                )
                            )
                            or original_df.loc[idx, "username"],
                            "first_name": nan_to_none(
                                cambios.get("first_name", {}).get(
                                    "after", original_df.loc[idx, "first_name"]
                                )
                            )
                            or original_df.loc[idx, "first_name"],
                            "last_name": nan_to_none(
                                cambios.get("last_name", {}).get(
                                    "after", original_df.loc[idx, "last_name"]
                                )
                            )
                            or original_df.loc[idx, "last_name"],
                            "roles": cambios.get("roles", {}).get(
                                "after", original_df.loc[idx, "roles"]
                            )
                            or original_df.loc[idx, "roles"],
                        }

                        # Realizar la solicitud PUT al backend
                        try:
                            response = requests.put(
                                f"{BACKEND_URL}/edit_user/{id_usuario}", json=data
                            )

                            if response.status_code == 200:
                                response_data = response.json()
                                placeholder_success.success(
                                    f":material/check: Usuario {response_data['username']} actualizado correctamente."
                                )
                            else:
                                st.error(
                                    f":material/gpp_maybe: Error al actualizar el usuario con ID {id_usuario}."
                                )
                        except requests.exceptions.RequestException as e:
                            placeholder_error.error(
                                ":material/gpp_maybe: Hubo un error al realizar la solicitud de actualización."
                            )

                    # Actualizar los DataFrames en el estado después de los cambios
                    st.session_state["original_roles_df"] = edited_df.copy()
                    st.session_state.users_df = edited_df.copy()
                    show_toast(
                        "Todos los datos han sido actualizados", icon=":material/check:"
                    )
                    time.sleep(2)
                    placeholder_info.empty()
                    placeholder_success.empty()
                    placeholder_warning.empty()
                    placeholder_error.empty()
                    load_users.clear()
                    update_users_in_yaml()
                    users = load_users()
                else:
                    placeholder_warning.warning(
                        "⚠️ No hay cambios entre los datos editados y los originales."
                    )
        with cols[1]:
            if st.button(
                ":material/refresh:",
                on_click=reset_df_user,
                use_container_width=True,
                key="btn_refresh_edit_user",
            ):
                del st.session_state.users_df
                del st.session_state.selected_user
                del st.session_state.selected_roles
                del st.session_state.df_u_key
                del st.session_state.original_roles_df

                # Recargar los usuarios y actualizar la tabla
                load_users.clear()
                users = load_users()
                users_data = []
                for user in users or []:
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
                st.session_state["df_u_key"] = str(
                    uuid.uuid4()
                )  # Generar nueva clave para evitar cache
                st.session_state["original_roles_df"] = (
                    users_df.copy()
                )  # Guardar el estado original
                st.session_state.selected_user = None  # Limpiar el usuario seleccionado
                st.session_state.selected_roles = []
                st.rerun()
    else:
        placeholder_warning.warning("⚠️ No hay usuarios disponibles en este momento.")
