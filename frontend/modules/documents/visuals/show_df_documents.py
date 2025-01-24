import streamlit as st
import json
import requests
import uuid
import pandas as pd
from modules.documents.utils.str_time import convert_datetime, convert_to_string
from modules.documents.utils.formatted_path import formatted_path
from modules.documents.decorators.get_documents_from_db import get_documents_from_db
from modules.documents.decorators.get_collections import get_collections
from modules.documents.utils.reset_df import reset_df

BACKEND_URL = st.secrets.get("BACKEND_URL", "Not found")


def show_df_documents():
    documents = get_documents_from_db()
    collections_names = get_collections()
    print("[show_df_documents - document-collections_names] ", collections_names)
    placeholder_info = st.empty()
    placeholder_success = st.empty()
    placeholder_warning = st.empty()
    placeholder_error = st.empty()

    placeholder_info.info(
        ":material/info: Por favor, edita los documentos antes de guardar los cambios."
    )

    if documents:
        # Convertir los documentos en un DataFrame para mostrarlos en una tabla editable
        documents_data = []
        for document in documents:
            formatted_directory = formatted_path(document["path"])
            created_at_datetime = convert_datetime(document["created_at"])
            document_url = f"{BACKEND_URL}/document/{document['name']}"
            documents_data.append(
                {
                    "id": document["id"],
                    "name": document["name"],
                    "collection_name": document["collection_name"],
                    "created_at": created_at_datetime,
                    "location": formatted_directory,
                    "view": document_url,
                }
            )

        # Convertir la lista de documentos a un DataFrame
        documents_df = pd.DataFrame(documents_data)

        # Guardar el dataframe original en session_state si no está guardado
        if "df_key" not in st.session_state:
            st.session_state["df_key"] = str(uuid.uuid4())

        # st.column_config.TextColumn(label=None, *, width=None, help=None, disabled=None, required=None, pinned=None, default=None, max_chars=None, validate=None)

        # st.column_config.LinkColumn(label=None, *, width=None, help=None, disabled=None, required=None, pinned=None, default=None, max_chars=None, validate=None, display_text=None)

        # st.column_config.SelectboxColumn(label=None, *, width=None, help=None, disabled=None, required=None, pinned=None, default=None, options=None)

        # st.column_config.DatetimeColumn(label=None, *, width=None, help=None, disabled=None, required=None, pinned=None, default=None, format=None, min_value=None, max_value=None, step=None, timezone=None)

        #!!!!!!!!!!!!!!!!!!!!!COLOCAR ATRIBUTOS FALTANTES EN TODAS LAS COLUMNAS!!!!!!!!!!!!!!!!!!
        # Mostrar la tabla con opciones de edición
        with st.spinner("Cargando archivos..."):
            edited_df = st.data_editor(
                documents_df.drop(columns=["id"]),
                column_config={
                    "name": st.column_config.TextColumn(
                        "Nombre del Documento",
                        required=True,
                        width="medium",
                        max_chars=100,
                    ),
                    "collection_name": st.column_config.SelectboxColumn(
                        label="Colección",
                        options=collections_names,
                        width="small",
                        help="Nombre de la colección a la que pertenece el documento",
                        required=True,
                        pinned=False,
                    ),
                    "created_at": st.column_config.DatetimeColumn(
                        label="Fecha de creación",
                        width=None,
                        help=None,
                        required=True,
                        min_value=None,
                        max_value=None,
                        step=None,
                        timezone=None,
                    ),
                    "location": st.column_config.TextColumn(
                        "Ubicación del Archivo",
                        width=None,
                        disabled=True,
                        required=True,
                        max_chars=100,
                    ),
                    "view": st.column_config.LinkColumn(
                        "Ver",
                        width="small",
                        display_text="💻",
                        required=True,
                        disabled=True,
                        max_chars=100,
                    ),
                },
                hide_index=True,
                use_container_width=True,
                num_rows="fixed",
                key=st.session_state.df_key,
            )

        # Compara las filas originales con las filas editadas
        rows_to_update = []
        for index, row in edited_df.iterrows():
            original_row = documents_df.iloc[index]  # type: ignore # Filas originales

            # Compara cada columna para ver si hubo algún cambio
            if (
                row["name"] != original_row["name"]
                or row["collection_name"] != original_row["collection_name"]
                or row["created_at"] != original_row["created_at"]
            ):

                rows_to_update.append(
                    {
                        "index": index,
                        "name": row["name"],
                        "collection_name": row["collection_name"],
                        "created_at": convert_to_string(row["created_at"]),
                    }
                )

        cols = st.columns([1, 1, 10], gap="small")
        with cols[0]:
            # Guardar cambios después de editar solo las filas modificadas
            if st.button(
                ":material/save:",
                use_container_width=True,
                key="btn_save_df_docs",
                type="primary",
            ):
                if rows_to_update:
                    with st.spinner("Guardando cambios..."):
                        for row in rows_to_update:
                            document_id = documents[row["index"]][
                                "id"
                            ]  # Supone que el `id` está disponible
                            data = {
                                "name": row["name"],
                                "collection_name": row["collection_name"],
                                "created_at": row["created_at"],
                            }
                            response = requests.put(
                                f"{BACKEND_URL}/edit_document/{document_id}", data=data
                            )
                            if response.status_code == 200:
                                placeholder_success.success(
                                    f"¡Documento '{row['name']}' actualizado correctamente!"
                                )
                            else:
                                placeholder_error.error(
                                    f"Error al actualizar el documento '{row['name']}'."
                                )
                    get_documents_from_db.clear()
                    get_collections.clear()
                    documents = get_documents_from_db()
                    collections = get_collections()
                else:
                    placeholder_warning.warning(
                        "No se detectaron cambios para actualizar."
                    )
        with cols[1]:
            st.button(
                ":material/refresh:",
                on_click=reset_df,
                use_container_width=True,
                key="btn_reset_df_docs",
            )
    else:
        placeholder_warning.warning("⚠️ No hay archivos disponibles en este momento.")
