import streamlit as st
import requests
import time
import json
import uuid
from modules.documents.decorators.get_documents_from_db import get_documents_from_db
from modules.documents.decorators.get_collections import get_collections
from modules.documents.utils.reset_uf import reset_uf
from helpers.show_toast import show_toast

BACKEND_URL = st.secrets.get("BACKEND_URL", "Not found")
MAX_FILES_UPLOAD = st.secrets.get("MAX_FILES_UPLOAD", 500)


def show_upload_docs():
    placeholder_info = st.empty()
    placeholder_success = st.empty()
    placeholder_error = st.empty()
    placeholder_warning = st.empty()
    placeholder_button2 = st.empty()
    # uploaded_files = st.file_uploader("Elige un archivo", type=['pdf', 'doc', 'docx', 'txt', 'rtf', 'odf', 'jpg', 'jpge', 'png', 'tif', 'tiff', 'gif', 'bmp', 'ppt', 'pptx', 'xls', 'xlsx'], accept_multiple_files=True, help="Seleccione los archivos")
    if "uf_key" not in st.session_state:
        st.session_state["uf_key"] = str(uuid.uuid4())

    placeholder_info.info(
        ":material/info: Puedes subir hasta "
        + str(MAX_FILES_UPLOAD)
        + " archivos cada vez"
    )
    uploaded_files = st.file_uploader(
        "Elige un archivo PDF",
        type=["pdf"],
        accept_multiple_files=True,
        help="Seleccione los archivos",
        key=st.session_state.uf_key,
    )

    if uploaded_files:
        if len(uploaded_files) > MAX_FILES_UPLOAD:
            placeholder_error.error(
                f":material/gpp_maybe: Solo puedes subir hasta {MAX_FILES_UPLOAD} archivos cada vez."
            )
            with placeholder_button2:
                if st.button("Recargar", type="primary", key="btn_recarga_2"):
                    placeholder_success.empty()
                    placeholder_error.empty()
                    placeholder_warning.empty()
                    reset_uf()
                    st.rerun()
        else:
            with st.spinner("Cargando..."):
                with st.expander("Documentos seleccionados"):
                    for uploaded_file in uploaded_files:
                        with st.container():
                            st.write(
                                f":material/upload_file: :orange[Nombre:] :violet[{uploaded_file.name}]"
                            )
                            st.write(
                                f":material/cloud_upload: :orange[Tamaño:] :violet[{uploaded_file.size / 1024:.2f} KB]"
                            )

            # Muestra el spinner durante la carga de colecciones
            with st.spinner("Obteniendo colecciones..."):
                collections = get_collections()

            # Selección de colección
            if not collections:
                placeholder_warning.warning("⚠️ No hay colecciones disponibles.")
                collection_name = st.text_input(
                    "Ingresa un nombre para una nueva colección"
                )
            else:
                collections.append("Crear Nueva")
                selected_option = st.selectbox("Selecciona una colección", collections)
                if selected_option == "Crear Nueva":
                    collection_name = st.text_input(
                        "Ingresa el nombre de la nueva colección"
                    )
                else:
                    collection_name = selected_option

            placeholder_button = st.empty()

            if st.button("Procesar", type="primary"):

                with st.container():
                    total_success_placeholder = st.empty()

                with st.container():
                    success_placeholder = st.empty()
                    success_messages = []

                with st.container():
                    total_error_placeholder = st.empty()

                with st.container():
                    error_placeholder = st.empty()
                    error_messages = []

                success_count = 0
                error_count = 0

                if collection_name:
                    for uploaded_file in uploaded_files:
                        with st.spinner(f"Procesando '{uploaded_file.name}'..."):
                            files = {
                                "file": (
                                    uploaded_file.name,
                                    uploaded_file,
                                    "application/pdf",
                                )
                            }
                            data = {"collection_name": collection_name}
                            response = requests.post(
                                f"{BACKEND_URL}/document", data=data, files=files
                            )

                        # Procesar la respuesta JSON del backend
                        try:
                            response_json = response.json()
                            status = response_json.get("status")
                            message = response_json.get("message", "Sin mensaje")

                            #!!!
                            execution_times = response_json.get("execution_times", {})
                            cpu_usage = response_json.get("cpu_usage", {})
                            memory_usage = response_json.get("memory_usage", {})
                            #!!!

                            if status == "Successfully Uploaded":
                                success_count += 1
                                with total_success_placeholder.container():
                                    st.success(
                                        f":material/check: {success_count} archivo(s) subido(s) correctamente."
                                    )
                                # success_messages.append(f":material/check: ¡Archivo '{uploaded_file.name}' subido correctamente!")
                                success_messages.append(
                                    f":material/check: ¡Archivo :green-background['{uploaded_file.name}'] subido correctamente!\n\n"
                                    f":blue-background[Tiempo de guardado]: {execution_times.get('save_time', 0):.2f} segundos.\n\n"
                                    f":blue-background[Tiempo de procesamiento]: {execution_times.get('process_time', 0):.2f} segundos.\n\n"
                                    f":orange-background[Uso inicial de CPU]: {cpu_usage.get('initial', 0)}%.\n\n"
                                    f":orange-background[Uso final de CPU]: {cpu_usage.get('final', 0)}%.\n\n"
                                    f":violet-background[Uso inicial de memoria]: {memory_usage.get('initial', 0)}%.\n\n"
                                    f":violet-background[Uso final de memoria]: {memory_usage.get('final', 0)}%"
                                )

                                with success_placeholder.popover(
                                    ":material/check: Detalle:"
                                ):
                                    if success_messages:
                                        for success_message in success_messages:
                                            st.write(f"{success_message}")
                                placeholder_warning.empty()
                            else:
                                error_count += 1
                                with total_error_placeholder.container():
                                    st.error(
                                        f":material/gpp_maybe: Se encontraron {error_count} error(es)."
                                    )
                                error_messages.append(
                                    f":material/gpp_maybe: Error al subir :red-background['{uploaded_file.name}]': {message}"
                                )
                                with error_placeholder.popover(
                                    ":material/gpp_maybe: Detalle:"
                                ):
                                    if error_messages:
                                        for error_message in error_messages:
                                            st.write(f"- {error_message}")
                        except ValueError:
                            error_count += 1
                            with total_error_placeholder.container():
                                st.error(
                                    f":material/gpp_maybe: Se encontraron {error_count} error(es)."
                                )
                            error_messages.append(
                                f":material/gpp_maybe: Error al procesar la respuesta del servidor para :red-background['{uploaded_file.name}']."
                            )
                            with error_placeholder.popover(
                                ":material/gpp_maybe: Detalle:"
                            ):
                                if error_messages:
                                    for error_message in error_messages:
                                        st.write(f"- {error_message}")

                    show_toast(
                        "El proceso de los archivos terminó", icon=":material/check:"
                    )
                    time.sleep(2)
                    get_documents_from_db.clear()
                    get_collections.clear()
                    placeholder_success.empty()
                    placeholder_error.empty()
                    placeholder_warning.empty()
                else:
                    placeholder_error.error(
                        ":material/gpp_maybe: Por favor ingresa un nombre para la colección."
                    )
            with placeholder_button:
                if st.button("Recargar", key="btn_recarga_1"):
                    placeholder_success.empty()
                    placeholder_error.empty()
                    placeholder_warning.empty()
                    reset_uf()
                    st.rerun()
