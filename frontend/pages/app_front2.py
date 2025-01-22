import streamlit as st
import requests
import asyncio
import websockets
import json
import io
import urllib.parse
import tempfile
import fitz
from PIL import Image
from streamlit_pdf_viewer import pdf_viewer

# URL del backend (ajusta según sea necesario)
BACKEND_URL = "http://localhost:8080"
BACKEND_WS_URL = "ws://localhost:8080/ws"


# Función para extraer imagen de una página del PDF
def extract_page_image(pdf_path, page_number):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_number - 1)  # PyMuPDF usa indexación 0
    pix = page.get_pixmap(dpi=300)  # type: ignore # Extraemos la imagen a 300 DPI
    img = Image.open(io.BytesIO(pix.tobytes()))
    return img


# Función para conectarse al WebSocket y enviar la consulta
async def ask_ollama(query):
    async with websockets.connect(BACKEND_WS_URL) as websocket:
        query_data = {"query": query}
        await websocket.send(json.dumps(query_data))
        try:
            response = await websocket.recv()
            response_data = json.loads(response)
            if response_data["event"] == "chunk":
                return response_data["content"]
            elif response_data["event"] == "finish":
                return "Respuesta completada."
        except Exception as e:
            return {"error": "Error al procesar la solicitud."}


# Título de la aplicación
st.title("Sistema RAG con LLM")

# Panel lateral de navegación
option = st.sidebar.radio(
    "Selecciona una opción",
    (
        "Subir PDF",
        "Consultar PDF",
        "Pregunta a la IA",
        "Pregunta a Ollama",
        "Gestionar Archivos",
    ),
)

# Subir un PDF
if option == "Subir PDF":
    st.header("Subir un PDF")
    uploaded_file = st.file_uploader("Elige un archivo PDF", type="pdf")

    if uploaded_file is not None:
        st.write(
            f"Archivo: {uploaded_file.name}, Tamaño: {uploaded_file.size / 1024:.2f} KB"
        )

        # Obtener las colecciones disponibles desde el backend
        response = requests.post(f"{BACKEND_URL}/collection_names")
        if response.status_code == 200:
            collections = response.json().get("collections", [])
        else:
            collections = []

        # Crear un selectbox para las colecciones disponibles o ingresar una nueva
        if not collections:
            st.warning("No hay colecciones creadas en la base de datos.")
            collection_name = st.text_input(
                "Ingresa el nombre para crear una nueva colección"
            )
        else:
            collections.append(
                "Personalizado"
            )  # Opción adicional para ingresar manualmente
            selected_option = st.selectbox("Selecciona una colección", collections)
            if selected_option == "Personalizado":
                collection_name = st.text_input(
                    "Ingresa el nombre de la nueva colección"
                )
            else:
                collection_name = selected_option

        # Botón para subir el archivo
        if st.button("Subir archivo"):
            if collection_name:
                with st.spinner("Subiendo el archivo..."):
                    files = {
                        "file": (uploaded_file.name, uploaded_file, "application/pdf")
                    }
                    data = {"collection_name": collection_name}
                    response = requests.post(
                        f"{BACKEND_URL}/pdf", data=data, files=files
                    )

                if response.status_code == 200:
                    st.success(
                        f"¡Archivo subido correctamente a la colección '{collection_name}'!"
                    )
                    st.json(response.json())
                else:
                    st.error("Error al subir el archivo.")
            else:
                st.error("Por favor ingresa un nombre para la colección.")

# Consultar un documento PDF
elif option == "Consultar PDF":
    st.header("Haga una pregunta sobre el PDF")
    query = st.text_input("Introduce tu consulta sobre el documento PDF")

    if st.button("Buscar"):
        if query:
            with st.spinner("Buscando..."):
                response = requests.post(
                    f"{BACKEND_URL}/ask_pdf", json={"query": query}
                )

            if response.status_code == 200:
                result = response.json()
                st.markdown(f"Llega hasta el frontend con este result: {result}")
                st.markdown(f"**Respuesta:** {result['answer']}")

                # Mostrar las fuentes de donde se obtuvo la información
                if "sources" in result and result["sources"]:
                    st.write("**Fuentes:**")
                    for source in result["sources"]:
                        file_path = urllib.parse.quote(
                            source.get("file_path", "Desconocido")
                        )
                        page_number = int(source.get("page_number", "Desconocido"))
                        st.markdown(
                            f"- **Documento:** {file_path} | **Página:** {page_number}"
                        )
                        pdf_url = f"{BACKEND_URL}/pdf/{file_path}"
                        pdf_response = requests.get(pdf_url)

                        if pdf_response.status_code == 200:
                            pdf_file = io.BytesIO(pdf_response.content)
                            with tempfile.NamedTemporaryFile(
                                delete=False, suffix=".pdf"
                            ) as temp_pdf_file:
                                temp_pdf_file.write(pdf_file.read())
                                temp_pdf_path = temp_pdf_file.name
                            page_img = extract_page_image(temp_pdf_path, page_number)
                            st.image(
                                page_img,
                                caption=f"Página {page_number} del documento",
                                use_container_width=True,
                            )

                            st.markdown(f"[Ver Documento Completo]({pdf_url})")
                            # Botón para abrir el documento completo
                            # if st.button(f"Ver documento completo ({file_path})"):
                            #     js_code = f"window.open('{pdf_url}', '_blank');"
                            #     st.components.v1.html(f"<script>{js_code}</script>", height=0)
                        else:
                            st.error("No se pudo descargar el archivo PDF.")
                else:
                    st.write("No se encontraron fuentes relevantes.")
            else:
                st.error("Error al obtener una respuesta. Intenta de nuevo.")
        else:
            st.error("Por favor, introduce una consulta.")


# Preguntar algo a la IA
elif option == "Pregunta a la IA":
    st.header("Hazle una pregunta a la IA")
    ai_query = st.text_input("Introduce tu pregunta a la IA")

    if st.button("Obtener respuesta de la IA"):
        if ai_query:
            with st.spinner("Obteniendo respuesta..."):
                response = requests.post(f"{BACKEND_URL}/ai", json={"query": ai_query})

            if response.status_code == 200:
                result = response.json()
                st.markdown(f"**Respuesta de la IA:** {result['answer']}")
            else:
                st.error("Error al obtener una respuesta de la IA.")
        else:
            st.error("Por favor, introduce una pregunta a la IA.")

# Preguntar algo a Ollama
elif option == "Pregunta a Ollama":
    st.header("Hazle una pregunta a Ollama")
    ollama_query = st.text_input("Introduce tu pregunta a Ollama")

    if st.button("Obtener respuesta de Ollama"):
        if ollama_query:
            with st.spinner("Obteniendo respuesta..."):
                try:
                    response = asyncio.run(ask_ollama(ollama_query))

                    if isinstance(response, dict) and "answer" in response:
                        st.markdown(f"**Respuesta de Ollama:** {response}")
                    else:
                        st.error("Error al obtener respuesta de Ollama.")
                except Exception as e:
                    st.error(f"Ocurrió un error al conectar con el servidor: {e}")
        else:
            st.error("Por favor, introduce una pregunta a Ollama.")

# Gestionar Archivos
elif option == "Gestionar Archivos":
    st.header("Gestión de Archivos")
    response = requests.get(f"{BACKEND_URL}/files")
    if response.status_code == 200:
        files_data = response.json()
        if files_data:
            selected_file = st.selectbox(
                "Selecciona un archivo para gestionar",
                [file["filename"] for file in files_data],
            )
            file_action = st.radio(
                "¿Qué te gustaría hacer con este archivo?",
                ("Eliminar", "Actualizar", "Ver"),
            )
            if file_action == "Eliminar":
                if st.button(f"Eliminar {selected_file}"):
                    response = requests.delete(f"{BACKEND_URL}/files/{selected_file}")
                    if response.status_code == 200:
                        st.success(
                            f"¡El archivo {selected_file} ha sido eliminado correctamente!"
                        )
                    else:
                        st.error("Error al eliminar el archivo.")
            elif file_action == "Actualizar":
                new_file = st.file_uploader(
                    "Elige un nuevo archivo PDF para reemplazar el actual", type="pdf"
                )
                if new_file:
                    files = {"file": new_file.getvalue()}
                    response = requests.put(
                        f"{BACKEND_URL}/files/{selected_file}", files={"file": new_file}
                    )
                    if response.status_code == 200:
                        st.success(
                            f"¡Archivo {selected_file} actualizado correctamente!"
                        )
                    else:
                        st.error("Error al actualizar el archivo.")
            elif file_action == "Ver":
                pdf_url = f"{BACKEND_URL}/pdf/{selected_file}"
                st.markdown(
                    f'<iframe src="{pdf_url}" width="700" height="500"></iframe>',
                    unsafe_allow_html=True,
                )
        else:
            st.warning("No hay archivos disponibles para gestionar.")
    else:
        st.error("Error al cargar la lista de archivos.")
