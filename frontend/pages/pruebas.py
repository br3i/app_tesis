
# !!!!!!!!!!!!!!!!!!!!PAGINACION EN DATAFRAME
# import streamlit as st
# import pandas as pd

# st.set_page_config(layout="centered")

# @st.cache_data(show_spinner=False)
# def load_data(file_path):
#     dataset = pd.read_csv(file_path)
#     return dataset


# @st.cache_data(show_spinner=False)
# def split_frame(input_df, rows):
#     df = [input_df.loc[i : i + rows - 1, :] for i in range(0, len(input_df), rows)]
#     return df


# file_path = st.file_uploader("Select CSV file to upload", type=["csv"])
# if file_path:
#     dataset = load_data(file_path)
#     top_menu = st.columns(3)
#     with top_menu[0]:
#         sort = st.radio("Sort Data", options=["Yes", "No"], horizontal=1, index=1)
#     if sort == "Yes":
#         with top_menu[1]:
#             sort_field = st.selectbox("Sort By", options=dataset.columns)
#         with top_menu[2]:
#             sort_direction = st.radio(
#                 "Direction", options=["⬆️", "⬇️"], horizontal=True
#             )
#         dataset = dataset.sort_values(
#             by=sort_field, ascending=sort_direction == "⬆️", ignore_index=True
#         )
#     pagination = st.container()

#     bottom_menu = st.columns((4, 1, 1))
#     with bottom_menu[2]:
#         batch_size = st.selectbox("Page Size", options=[25, 50, 100])
#     with bottom_menu[1]:
#         total_pages = (
#             int(len(dataset) / batch_size) if int(len(dataset) / batch_size) > 0 else 1
#         )
#         current_page = st.number_input(
#             "Page", min_value=1, max_value=total_pages, step=1
#         )
#     with bottom_menu[0]:
#         st.markdown(f"Page **{current_page}** of **{total_pages}** ")



#     pages = split_frame(dataset, batch_size)
#     pagination.dataframe(data=pages[current_page - 1], use_container_width=True)











#!!!!!!!!!!!!!!!USO DE ECHO PARA EL CODIGO

# import streamlit as st

# def get_user_name():
#     return 'John'

# with st.echo():
#     # Everything inside this block will be both printed to the screen
#     # and executed.

#     def get_punctuation():
#         return '!!!'

#     greeting = "Hi there, "
#     value = get_user_name()
#     punctuation = get_punctuation()

#     st.write(greeting, value, punctuation)

# # And now we're back to _not_ printing to the screen
# foo = 'bar'
# st.write('Done!')




#!!!!!!!!!!!!!!RESTART UPLOAD_FILE
# import streamlit as st

# if "file_uploader_key" not in st.session_state:
#     st.session_state["file_uploader_key"] = 0

# if "uploaded_files" not in st.session_state:
#     st.session_state["uploaded_files"] = []

# files = st.file_uploader(
#     "Upload some files",
#     accept_multiple_files=True,
#     key=st.session_state["file_uploader_key"],
# )

# if files:
#     st.session_state["uploaded_files"] = files

# if st.button("Clear uploaded files"):
#     st.session_state["file_uploader_key"] += 1
#     st.rerun()

# st.write("Uploaded files:", st.session_state["uploaded_files"])




















#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# import streamlit as st
# import pandas as pd

# # Datos iniciales
# data = [
#     {"id": 1, "username": "user1", "roles": ["admin"]},
#     {"id": 2, "username": "user2", "roles": ["viewer"]},
#     {"id": 3, "username": "user3", "roles": ["user", "viewer"]},
# ]
# users_df = pd.DataFrame(data)

# # Cargar estado inicial si no existe
# if "users_df" not in st.session_state:
#     st.session_state.users_df = users_df

# if "selected_user" not in st.session_state:
#     st.session_state.selected_user = None

# # Seleccionar usuario
# selected_user = st.selectbox(
#     "Seleccione un usuario para editar",
#     options=st.session_state.users_df["username"].tolist(),
#     index=0 if st.session_state.selected_user is None else st.session_state.users_df[
#         st.session_state.users_df["username"] == st.session_state.selected_user
#     ].index[0],
#     key="user_selector",
# )

# # Mostrar roles del usuario seleccionado
# user_data = st.session_state.users_df[
#     st.session_state.users_df["username"] == selected_user
# ]
# roles = user_data["roles"].iloc[0]  # Obtener los roles actuales

# # Editar roles
# updated_roles = st.multiselect(
#     "Seleccione los roles para el usuario",
#     options=["admin", "user", "viewer"],
#     default=roles,
#     key="roles_editor",
# )

# # Botón para actualizar
# if st.button("Actualizar"):
#     # Usar `.apply()` para actualizar correctamente la columna `roles`
#     st.session_state.users_df.loc[
#         st.session_state.users_df["username"] == selected_user, "roles"
#     ] = st.session_state.users_df.loc[
#         st.session_state.users_df["username"] == selected_user, "roles"
#     ].apply(lambda x: updated_roles)

#     # Reflejar los cambios en la UI
#     st.success(f"Roles de {selected_user} actualizados a: {updated_roles}")

# # Mostrar el DataFrame actualizado
# st.data_editor(
#     st.session_state.users_df,
#     column_config={
#         "id": st.column_config.TextColumn(label="ID", disabled=True),
#         "username": st.column_config.TextColumn(
#             label="Nombre de Usuario", disabled=True
#         ),
#         "roles": st.column_config.TextColumn(label="Roles", disabled=True),
#     },
#     use_container_width=True,
# )











#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!DOCUMENTACION DE LA FUNCION EDITAR USUARIOS
# import streamlit as st
# import json
# import requests
# import uuid
# import numpy as np
# import pandas as pd
# from modules.user.decorators.get_roles import get_roles
# from modules.user.utils.reset_df_user import reset_df_user
# from modules.log_in.config_data.config_data import update_users_in_yaml
# from modules.log_in.cache_data.load_data import load_users


# BACKEND_URL = st.secrets.get('BACKEND_URL', 'Not found')
# MAX_FIRSTNAME_LENGTH = int(st.secrets.get('MAX_FIRSTNAME_LENGTH', 'Not found'))
# MAX_LASTNAME_LENGTH = int(st.secrets.get('MAX_LASTNAME_LENGTH', 'Not found'))
# MAX_USERNAME_LENGTH = int(st.secrets.get('MAX_USERNAME_LENGTH', 'Not found'))



# def convert_int64_to_int(value):
#     # Convertir cualquier valor int64 a int de Python
#     if isinstance(value, (np.int64, pd.Timestamp)):  # Para int64 y Timestamps
#         return int(value)
#     return value

# def nan_to_none(value):
#     """Convierte NaN en None para ser JSON serializable."""
#     if isinstance(value, float) and np.isnan(value):
#         return None
#     return value

# def procesar_cambios(idx, differences_roles, differences, edited_df, original_df):
#     """
#     Procesa los cambios detectados en roles y otros campos, construyendo un diccionario de cambios.
#     """
#     # Obtener ID del usuario afectado
#     id_usuario = original_df.loc[idx, 'id']
#     cambios = {}

#     # Procesar cambios en roles si existen
#     if not differences_roles.empty and idx in differences_roles.index:
#         cambios_fila_roles = differences_roles.loc[idx]
#         cambios["roles"] = {
#             "after": nan_to_none(cambios_fila_roles.get(("roles", "self"), edited_df.loc[idx, "roles"])),
#             "before": nan_to_none(cambios_fila_roles.get(("roles", "other"), original_df.loc[idx, "roles"]))
#         }

#     # Procesar cambios en otros campos si existen
#     if not differences.empty and idx in differences.index:
#         cambios_fila_otros = differences.loc[idx]
#         for col in differences.columns.get_level_values(0).unique():
#             cambios[col] = {
#                 "after": nan_to_none(cambios_fila_otros.get((col, "self"), edited_df.loc[idx, col])),
#                 "before": nan_to_none(cambios_fila_otros.get((col, "other"), original_df.loc[idx, col]))
#             }

#     return id_usuario, cambios

# def show_df_users():
#     # Obtener datos de usuarios y roles
#     users = load_users()  # Cargar usuarios
#     roles = get_roles()  # Obtener roles
#     options_roles = roles['roles']  # Lista de roles disponibles
#     print("\n-----------------------------------------------------------")
#     print("\n\n[options_roles] : ", options_roles)
    
#     placeholder_info = st.empty()
#     placeholder_success = st.empty()
#     placeholder_warning = st.empty()
#     placeholder_error = st.empty()

#     placeholder_info.info("Por favor, edita los usuarios antes de guardar los cambios.")

#     if users:
#         # Convertir los documentos en un DataFrame para mostrarlos en una tabla editable
#         users_data = []
#         for user in users:
#             users_data.append({
#                 "id": user['id'],
#                 "email": user['email'],
#                 "username": user['username'],
#                 "first_name": user['first_name'],
#                 "last_name": user['last_name'],
#                 "roles": user['roles'],  # Mantener roles como lista
#             })
        
#         # Convertir la lista de usuarios a un DataFrame
#         users_df = pd.DataFrame(users_data)
#         print("\n\n[users_df] : \n", users_df)

            

#         # Guardar una copia en session_state
#         if "users_df" not in st.session_state:
#             st.session_state.users_df = users_df.copy()  # Guardar la copia del DataFrame
#         if "selected_user" not in st.session_state:
#             st.session_state.selected_user = None
#         if "selected_roles" not in st.session_state:
#             st.session_state.selected_roles = []
#         if 'df_u_key' not in st.session_state:
#             st.session_state['df_u_key'] = str(uuid.uuid4())
#         #!!!!!
#         if 'original_roles_df' not in st.session_state:
#             st.session_state['original_roles_df'] = st.session_state['users_df'].copy()
#         #!!!!!
        
#         # Crear una copia independiente de los datos originales
#         original_df = st.session_state.users_df.copy()

#         # Depuración del estado de session_state antes de la edición
#         print("\n\n[session_state] (antes de la edición) : \n", st.session_state)

#         # Asegúrate de que la columna 'roles' siempre sea una lista de cadenas
#         st.session_state.users_df['roles'] = st.session_state.users_df['roles'].apply(
#             lambda x: x if isinstance(x, list) else (x.split(', ') if isinstance(x, str) else [])
#         )
        
#         print("\n[roles después de la transformación] : \n", st.session_state.users_df['roles'])

#         with st.status("Valores en st.session_state"):
#             st.write(st.session_state.users_df)
#             st.write(users_df)
#             st.session_state['original_roles_df']

#         # Sección de edición de roles
#         with st.expander("Edición de Roles"):
#             col1, col2 = st.columns([0.3, 0.7], gap="small", vertical_alignment="center")
            
#             with col1:
#                 # Seleccionar un usuario
#                 selected_user = st.selectbox(
#                     "Seleccione un usuario",
#                     options=st.session_state.users_df["username"].tolist(),
#                     index=0 if st.session_state.selected_user is None else st.session_state.users_df[
#                         st.session_state.users_df["username"] == st.session_state.selected_user
#                     ].index[0],
#                     key="user_selector",
#                 )

#                 # Obtener roles del usuario seleccionado
#                 user_roles = st.session_state.users_df[
#                     st.session_state.users_df["username"] == selected_user
#                 ]["roles"].iloc[0]

#                 # Asignar roles actuales al estado
#                 st.session_state.selected_roles = user_roles if isinstance(user_roles, list) else user_roles.split(", ")
#                 print("\n\n[selected_roles]: \n", st.session_state.selected_roles)

#             with col2:
#                 # Editar roles
#                 updated_roles = st.multiselect(
#                     "Seleccione los roles para el usuario"  ,
#                     options=options_roles,
#                     default=st.session_state.selected_roles,
#                     key="roles_editor",
#                 )

#             # Botón para actualizar los roles
#             if st.button("Actualizar Tabla"):
#                 print("           {}{}{}{}{}{}{}{}{}{}{}{}{}       ")
#                 print("\n\n[actualizar tabla_updated_roles]: \n", updated_roles)
#                 print("\n\n[actualizar selected_user]: \n", selected_user)
#                 # Actualizar los roles en el DataFrame
#                 #!!!!
#                 st.session_state.users_df.loc[
#                     st.session_state.users_df["username"] == selected_user, "roles"
#                 ] = ", ".join(updated_roles)
#                 print("\n\n[actualizar_tabla st.ss.users_df-roles] : \n", st.session_state.users_df['roles'])
#                 #!!!!!!!!
#                 st.success(f"Roles del usuario '{selected_user}' actualizados correctamente.")
#                 st.session_state.selected_roles = updated_roles  # Actualizar roles seleccionados
#                 st.session_state.users_df = st.session_state.users_df.copy()  # Mantener la copia actualizada
#                 #st.rerun()
        
#         # Asegurarse de que la columna 'roles' siempre sea una lista de cadenas
#         st.session_state.users_df['roles'] = st.session_state.users_df['roles'].apply(
#             lambda x: x if isinstance(x, list) else (x.split(', ') if isinstance(x, str) else [])
#         )
        
#         try:
#             print("\n\n[edited_df] (antes de la edición) : \n", edited_df)
#         except NameError:
#             print("\n\n[Error] La variable 'edited_pf' no estaba definida")

#         # Mostrar los datos en un data_editor editable
#         edited_df = st.data_editor(
#             st.session_state.users_df,
#             column_config={
#                 "username": st.column_config.TextColumn("Usuario", required=True, width="small", max_chars=MAX_USERNAME_LENGTH),
#                 "email": st.column_config.TextColumn("Email", required=True, width="small"),
#                 "first_name": st.column_config.TextColumn("Primer Nombre", required=True, width="small", max_chars=MAX_FIRSTNAME_LENGTH),
#                 "last_name": st.column_config.TextColumn("Apellido", required=True, width="small", max_chars=MAX_LASTNAME_LENGTH),
#                 #"roles": st.column_config.TextColumn("Roles", disabled=True, required=True),
#                 "roles": st.column_config.ListColumn(label="Rol",width="small",help="Rol asigando al usuario",pinned=False,),
#             },
#             hide_index=True,
#             use_container_width=True,
#             num_rows="fixed",
#             key = "data_editor_static_key"
#             #key=st.session_state.df_u_key,
#         )

#         # Verificación de los datos después de la edición
#         print("\n\n[edited_df] (después de la edición) : \n", edited_df)  # Verificación de los cambios

#         # Botón para guardar cambios
#         if st.button("Guardar Cambios"):
#             print("\n\n           ++++++++++++++++++++++++++++++++++           ")
#             print("\n[COMPARACION CAMBIOS]\n")
#             print("\n\n[edited_df]: \n", edited_df)
#             print("\n\n[users_df]: \n", st.session_state.users_df)
#             print("\n\n[original_df]: \n", original_df)
#             print("\n\n[st.ss.st['original_roles_df']]: \n", st.session_state['original_roles_df'])


#             # Comparar los DataFrames para identificar diferencias
#             differences_roles = edited_df.compare(st.session_state["original_roles_df"])
#             differences = edited_df.compare(original_df)

#             # Verificar si hay cambios en roles o en otros campos
#             if not differences_roles.empty or not differences.empty:
#                 print("\n\n[Procesando cambios detectados]")
#                 st.info("⚠️ Se encontraron diferencias entre los datos editados y los originales. Revisa la consola para más detalles.")

#                 for idx in set(differences_roles.index).union(differences.index):
#                     id_usuario, cambios = procesar_cambios(idx, differences_roles, differences, edited_df, original_df)
#                     print(f"\n[ID Usuario]: {id_usuario}")
#                     print(f"Usuario con ID {id_usuario} tiene cambios: {cambios}")

#                     # Revisión de tipos y valores antes de construir 'data'
#                     for campo, valor in cambios.items():
#                         print(f"[DEBUG] Cambios para '{campo}': {valor}")
#                         print(f"[DEBUG] Tipo de 'after' para '{campo}': {type(valor.get('after'))}")
#                         print(f"[DEBUG] Tipo de 'before' para '{campo}': {type(valor.get('before'))}")


#                     # Construir el JSON para la solicitud
#                     data = {
#                         "id": convert_int64_to_int(id_usuario),
#                         "email": nan_to_none(cambios.get("email", {}).get("after", original_df.loc[idx, "email"])) or original_df.loc[idx, "email"],
#                         "username": nan_to_none(cambios.get("username", {}).get("after", original_df.loc[idx, "username"])) or original_df.loc[idx, "username"],
#                         "first_name": nan_to_none(cambios.get("first_name", {}).get("after", original_df.loc[idx, "first_name"])) or original_df.loc[idx, "first_name"],
#                         "last_name": nan_to_none(cambios.get("last_name", {}).get("after", original_df.loc[idx, "last_name"])) or original_df.loc[idx, "last_name"],
#                         "roles": cambios.get("roles", {}).get("after", original_df.loc[idx, "roles"]) or original_df.loc[idx, "roles"],
#                     }
#                     print(f"[Datos para actualizar Usuario ID {id_usuario}]: {data}")

#                     print(f"[DEBUG] Datos para actualizar Usuario ID {id_usuario}: {data}")
#                     print(f"[DEBUG] Tipo de 'roles': {type(data['roles'])}")
#                     print(f"[DEBUG] Tipo de 'email': {type(data['email'])}")
#                     print(f"[DEBUG] Tipo de 'last_name': {type(data['last_name'])}")

#                     # Realizar la solicitud PUT al backend
#                     try:
#                         response = requests.put(f"{BACKEND_URL}/edit_user/{id_usuario}", json=data)

#                         # Manejo de respuesta
#                         print(f"[Respuesta de la solicitud PUT] Status Code: {response.status_code}")
#                         print(f"[Respuesta de la solicitud PUT] Contenido: {response.text}")

#                         if response.status_code == 200:
#                             print(f"Usuario con ID {id_usuario} actualizado exitosamente.")
#                             st.success(f"✅ Usuario con ID {id_usuario} actualizado correctamente.")
#                         else:
#                             print(f"Error al actualizar el usuario con ID {id_usuario}: {response.text}")
#                             st.error(f"⚠️ Error al actualizar el usuario con ID {id_usuario}.")
#                     except requests.exceptions.RequestException as e:
#                         print(f"Error en la solicitud: {e}")
#                         st.error("⚠️ Hubo un error al realizar la solicitud de actualización.")

#                 # Actualizar los DataFrames en el estado después de los cambios
#                 st.session_state["original_roles_df"] = edited_df.copy()
#                 st.session_state.users_df = edited_df.copy()
#                 print(f"[Nuevo DataFrame en session_state]: \n{st.session_state.users_df}")
#                 st.success("✅ Datos actualizados correctamente en el estado.")
#             else:
#                 print("\n\n[Sin diferencias] Los datos editados coinciden con los originales.")
#                 st.success("✅ No hay cambios entre los datos editados y los originales.")      
#     else:
#         placeholder_warning.warning("⚠️ No hay archivos disponibles en este momento.")

# show_df_users()





























































import streamlit as st

# Ejemplo de valores para las variables
key = 1
value = 2

# Configuración de columnas con un ajuste de tamaño
col3, col4, col5, col6 = st.columns([2, 2, 1, 1])

# Utilizamos CSS para asegurar que todo se alinee correctamente
with st.sidebar:
    with col3:
        # Alineación vertical y horizontal utilizando CSS
        st.markdown(f"<div style='display: flex; justify-content: center; align-items: center; height: 100%; font-size: 20px; font-weight: bold;'>{key}</div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div style='display: flex; justify-content: center; align-items: center; height: 100%; font-size: 20px;'>{value}</div>", unsafe_allow_html=True)
    with col5:
        st.markdown(f"<div style='display: flex; justify-content: center; align-items: center; height: 100%;'></div>", unsafe_allow_html=True)
        thumbs_down_button = st.button("👎")
    with col6:
        st.markdown(f"<div style='display: flex; justify-content: center; align-items: center; height: 100%;'></div>", unsafe_allow_html=True)
        thumbs_up_button = st.button("👍")
