import streamlit as st
import tempfile
import io
import urllib.parse
import requests
from modules.chat.utils.extract_page_image import extract_page_image

BACKEND_URL = st.secrets.get("BACKEND_URL", "Not Found")

#!!!! Que sea un selectbox y pida los elementos del backend
# def model_selector(modelos):


def show_sources(sources):
    # Comprobar si existen fuentes
    if sources:
        # print(f"[\n\n\show_chat_component]: {sources}\n\n\n")
        # Mostrar el número de fuentes encontradas en el mensaje de estado
        with st.status(f"Obteniendo fuentes. Encontradas: {len(sources)}"):
            for source in sources:
                # Decodificar el nombre del archivo para mostrarlo correctamente
                # readable_file_path = urllib.parse.unquote(source.get("file_path", "Desconocido"))
                readable_document_name = urllib.parse.unquote(
                    source.get("document_name", "Desconocido")
                )
                # print(f"[\n\n\nUSER_UTILS]readable_file_path: {readable_document_name}\n\n\n")
                resolve_page = int(source.get("resolve_page", "Desconocido"))
                st.markdown(
                    f"- :violet[Documento]: {readable_document_name} | :orange[Página]: {resolve_page}"
                )

                # Codificar el nombre del archivo para usarlo en la URL
                encoded_document_name = urllib.parse.quote(
                    readable_document_name, "Desconocido"
                )
                # print(f"[\n\n\nUSER_UTILS]encoded_document_name: {encoded_document_name}\n\n\n")
                document_url = f"{BACKEND_URL}/document/{encoded_document_name}.pdf"
                # print(f"[\n\n\nUSER_UTILS]document_url: {document_url}\n\n")
                document_response = requests.get(document_url)

                if document_response.status_code == 200:
                    document_file = io.BytesIO(document_response.content)
                    with tempfile.NamedTemporaryFile(
                        delete=False, suffix=".pdf"
                    ) as temp_document_file:
                        temp_document_file.write(document_file.read())
                        temp_document_path = temp_document_file.name
                    page_img = extract_page_image(temp_document_path, resolve_page)
                    col1, col2, col3 = st.columns([0.15, 0.7, 0.15])
                    with col2:
                        st.image(
                            page_img,
                            caption=f"Página {resolve_page} del documento",
                            use_container_width=True,
                        )
                        st.markdown(
                            f"[:gray-background[Documento Completo]]({document_url})"
                        )
                else:
                    st.error("No se pudo descargar el archivo PDF.")
    else:
        # Si no hay fuentes, mostrar un mensaje de error
        with st.status("Obteniendo fuentes. Ninguna fuente encontrada."):
            st.write("No se encontraron fuentes relevantes.")
