import streamlit as st
import io
import json
import urllib.parse
import requests
import websocket
import base64
from PIL import Image

BACKEND_URL = st.secrets.get("BACKEND_URL", "Not Found")
BACKEND_WS_URL = st.secrets.get("BACKEND_WS_URL", "Not Found")

#!!!! Que sea un selectbox y pida los elementos del backend
# def model_selector(models_ollama):


#!! Solo con request
# def show_sources(sources):
#     # Comprobar si existen fuentes
#     if sources:
#         # print(f"[\n\n\show_chat_component]: {sources}\n\n\n")
#         # Mostrar el número de fuentes encontradas en el mensaje de estado
#         with st.status(f"Obteniendo fuentes. Encontradas: {len(sources)}"):
#             for source in sources:
#                 # Decodificar el nombre del archivo para mostrarlo correctamente
#                 # readable_file_path = urllib.parse.unquote(source.get("file_path", "Desconocido"))
#                 readable_document_name = urllib.parse.unquote(
#                     source.get("document_name", "Desconocido")
#                 )
#                 # print(f"[\n\n\nUSER_UTILS]readable_file_path: {readable_document_name}\n\n\n")
#                 resolve_page = int(source.get("resolve_page", "Desconocido"))
#                 st.markdown(
#                     f"- :violet[Documento]: {readable_document_name} | :orange[Página]: {resolve_page}"
#                 )

#                 # Hacer la solicitud al backend para obtener la imagen de la página
#                 document_url = f"{BACKEND_URL}/get_page_image?file_path={urllib.parse.quote(source['file_path'])}&resolve_page={resolve_page}"
#                 document_response = requests.get(document_url)

#                 if document_response.status_code == 200:
#                     # Mostrar la imagen recibida
#                     img = document_response.content
#                     cols = st.columns([0.1, 0.8, 0.1], gap="small")
#                     with cols[1]:
#                         st.image(
#                             img,
#                             caption=f"Página {resolve_page} del documento",
#                             use_container_width=True,
#                         )
#                         st.markdown(
#                             f"[:gray-background[Documento Completo]]({BACKEND_URL}/document/{urllib.parse.quote(readable_document_name)}.pdf)"
#                         )
#                 else:
#                     st.error("No se pudo obtener la imagen de la página del documento.")
#     else:
#         # Si no hay fuentes, mostrar un mensaje de error
#         with st.status("Obteniendo fuentes. Ninguna fuente encontrada."):
#             st.write("No se encontraron fuentes relevantes.")


def show_sources_via_ws(sources):
    if sources:
        with st.status("Obteniendo imágenes..."):
            try:
                # Establecer conexión WebSocket
                ws = websocket.create_connection(f"{BACKEND_WS_URL}/get_page_images")

                # Enviar la lista de solicitudes
                batch_request_data = [
                    {
                        "file_path": source.get("file_path", ""),
                        "resolve_page": int(source.get("resolve_page", 1)),
                    }
                    for source in sources
                ]

                ws.send(json.dumps(batch_request_data))

                # Recibir y mostrar imágenes progresivamente
                for index in range(len(sources)):
                    print(
                        f"Recibiendo mensaje del WebSocket... (Iteración {index + 1}/{len(sources)})"
                    )
                    message = ws.recv()
                    data = json.loads(message)

                    # Verificar si hubo un error
                    if "error" in data:
                        print(f"Error en los datos recibidos: {data['error']}")
                        st.error(f"Error: {data['error']}")
                        continue

                    # Decodificar la imagen base64
                    img_base64 = data.get("image", None)
                    if img_base64:
                        print("Imagen encontrada, decodificando...")
                        img_bytes = base64.b64decode(img_base64)
                        img = Image.open(io.BytesIO(img_bytes))
                        document_name = data.get("document_name", "Desconocido")
                        resolve_page = data.get("resolve_page", "Desconocido")

                        st.markdown(
                            f"- :violet[Documento]: {document_name} | :orange[Página]: {resolve_page}"
                        )
                        cols = st.columns([0.1, 0.8, 0.1], gap="small")
                        with cols[1]:
                            st.image(
                                img,
                                caption=f"Página {resolve_page} del documento",
                                use_container_width=True,
                            )
                    else:
                        print(
                            f"No se pudo cargar la imagen de la página {data.get('resolve_page', 'Desconocido')}"
                        )
                        st.error(
                            f"No se pudo cargar la imagen de la página {data.get('resolve_page', 'Desconocido')} del documento."
                        )
            except Exception as e:
                print(f"Error durante la ejecución: {e}")
                st.error(f"Error en la conexión WebSocket: {e}")
    else:
        st.info("No se encontraron fuentes relevantes.")
