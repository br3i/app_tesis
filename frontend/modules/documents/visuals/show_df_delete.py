import streamlit as st
import uuid
import pandas as pd
import requests
from modules.documents.utils.formatted_path import formatted_path
from modules.documents.decorators.get_documents_from_db import get_documents_from_db
from modules.documents.decorators.get_collections import get_collections
from modules.documents.utils.reset_df_dlt import reset_df_dlt

BACKEND_URL = st.secrets.get("BACKEND_URL", "Not found")


def show_df_delete():
    documents = get_documents_from_db()  # Obtener los documentos de la base de datos
    collections_names = get_collections()
    placeholder_info = st.empty()
    placeholder_success = st.empty()
    placeholder_warning = st.empty()
    placeholder_error = st.empty()

    placeholder_info.info(
        ":material/info: Por favor, selecciona los documentos que deseas eliminar."
    )

    if documents:
        # Convertir los documentos en un DataFrame para mostrarlos en una tabla editable
        documents_data = []
        for document in documents:
            formatted_directory = formatted_path(document["path"])
            document_url = f"{BACKEND_URL}/pdf/{document['name']}"
            documents_data.append(
                {
                    "id": document["id"],
                    "name": document["name"],
                    "collection_name": document["collection_name"],
                    "location": formatted_directory,
                    "view": document_url,
                    "Eliminar": False,
                }
            )

        # Convertir la lista de documentos a un DataFrame
        documents_df = pd.DataFrame(documents_data)

        # Guardar el dataframe original en session_state si no está guardado
        if "df_key_dlt" not in st.session_state:
            st.session_state["df_key_dlt"] = str(uuid.uuid4())

        # Mostrar la tabla con opciones de selección
        with st.spinner("Cargando archivos..."):
            selected_df = st.data_editor(
                documents_df.drop(columns=["id"]),
                column_config={
                    "Eliminar": st.column_config.CheckboxColumn(
                        "Eliminar",
                        help="Seleccione para eliminar",
                        default=False,
                    ),
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
                key=st.session_state.df_key_dlt,
            )

        # Filtrar los documentos seleccionados para eliminar
        rows_to_delete = []
        for index, row in selected_df.iterrows():
            if row["Eliminar"]:  # Si el checkbox está marcado
                document_id = documents_df.at[index, "id"]
                rows_to_delete.append(
                    {
                        "index": index,
                        "document_id": document_id,  # El id del documento a eliminar
                    }
                )

        # Columna para los botones de acción
        cols = st.columns([1, 1, 10], gap="small")
        with cols[0]:
            # Eliminar los documentos seleccionados
            if st.button(":material/delete:", key="btn_dlt_docs", type="primary"):
                if rows_to_delete:
                    with st.spinner("Eliminando documentos..."):
                        for row in rows_to_delete:
                            document_id = row["document_id"]
                            response = requests.delete(
                                f"{BACKEND_URL}/delete_document/{document_id}"
                            )
                            if response.status_code == 200:
                                placeholder_success.success(
                                    f":material/check: ¡Documento '{documents[row['index']]['name']}' eliminado correctamente!"
                                )
                            else:
                                st.error(
                                    f":material/gpp_maybe: Error al eliminar el documento '{documents[row['index']]['name']}'."
                                )
                    get_documents_from_db.clear()
                    documents = get_documents_from_db()
                    st.rerun()
                else:
                    placeholder_warning.warning(
                        "⚠️ No se detectaron documentos seleccionados para eliminar."
                    )
        with cols[1]:
            st.button(
                ":material/refresh:", on_click=reset_df_dlt, key="btn_reset_dlt_docs"
            )
    else:
        placeholder_warning.warning("⚠️ No hay archivos disponibles en este momento.")
