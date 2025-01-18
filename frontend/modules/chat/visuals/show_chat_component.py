import streamlit as st
import tempfile
import io
import urllib
import requests
from modules.chat.utils.extract_page_image import extract_page_image

BACKEND_URL = st.secrets.get("BACKEND_URL", "Not Found")

def model_selector(models_ollama):
    if "models" in models_ollama:
        # Filtrar modelos que generan respuestas y excluir familias específicas
        response_models = [
            {
                "name": model.model,
                "size": model.size,
                "family": model.details.family,
            }
            for model in models_ollama["models"]
            if model.details.family not in ["bert", "nomic-bert"]  # Excluir familias de embeddings
        ]

        if response_models:
            # Controles para ordenamiento y búsqueda
            col1, col2, col3 = st.columns(3)

            with col1:
                search_query = st.text_input(
                    "Búsqueda de Modelos:",
                    value="",
                    placeholder="Escriba el nombre de un modelo...",
                    help="Escriba algo para filtrar los modelos."
                )
            with col2:
                sort_direction = st.selectbox(
                    "Dirección de Orden:",
                    ("Ascendente", "Descendente"),
                    index=0
                )
            with col3:
                sort_option = st.selectbox(
                    "Ordenar por:",
                    ("Alfabéticamente", "Por Tamaño"),
                    index=0
                )
            
            # Filtrar modelos según el término de búsqueda
            filtered_models = [
                model for model in response_models
                if search_query.lower() in model["name"].lower()
            ] if search_query else response_models

            # Determinar si el orden es ascendente o descendente
            reverse_order = sort_direction == "Descendente"

            # Ordenar la lista de modelos según el criterio seleccionado
            if sort_option == "Alfabéticamente":
                filtered_models = sorted(filtered_models, key=lambda x: x["name"].lower(), reverse=reverse_order)
            elif sort_option == "Por Tamaño":
                filtered_models = sorted(filtered_models, key=lambda x: x["size"], reverse=reverse_order)

            if filtered_models:
                # Crear un selectbox que muestra detalles adicionales pero selecciona solo el nombre del modelo
                formatted_models = [
                    f"{model['name']} | Size: {model['size'] / 1_000_000:.2f} MB | Family: {model['family']}"
                    for model in filtered_models
                ]
                selected_index = st.selectbox(
                    "Please select the model:",
                    range(len(formatted_models)),
                    format_func=lambda i: formatted_models[i],
                )
                st.session_state.selected_model = filtered_models[selected_index]["name"]
            else:
                st.warning("No models match your search query.")
        else:
            st.error("No suitable models found for response generation.")
    else:
        st.error("No models found in the response.")

def show_sources(sources):
    # Comprobar si existen fuentes
    if sources:
        print(f"[\n\n\nUSER_UTILS]: {sources}\n\n\n")
        # Mostrar el número de fuentes encontradas en el mensaje de estado
        with st.status(f"Obteniendo fuentes. Encontradas: {len(sources)}"):
            for source in sources:
                # Decodificar el nombre del archivo para mostrarlo correctamente
                # readable_file_path = urllib.parse.unquote(source.get("file_path", "Desconocido"))
                readable_document_name = urllib.parse.unquote(source.get("document_name", "Desconocido"))
                print(f"[\n\n\nUSER_UTILS]readable_file_path: {readable_document_name}\n\n\n")
                resolve_page = int(source.get("resolve_page", "Desconocido"))
                st.markdown(f"- :violet[Documento]: {readable_document_name} | :orange[Página]: {resolve_page}")
                
                # Codificar el nombre del archivo para usarlo en la URL
                encoded_document_name = urllib.parse.quote(readable_document_name, "Desconocido")
                print(f"[\n\n\nUSER_UTILS]encoded_document_name: {encoded_document_name}\n\n\n")
                document_url = f"{BACKEND_URL}/document/{encoded_document_name}.pdf"
                print(f"[\n\n\nUSER_UTILS]document_url: {document_url}\n\n")
                document_response = requests.get(document_url)

                if document_response.status_code == 200:
                    document_file = io.BytesIO(document_response.content)
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_document_file:
                        temp_document_file.write(document_file.read())
                        temp_document_path = temp_document_file.name
                    page_img = extract_page_image(temp_document_path, resolve_page)
                    col1, col2, col3 = st.columns([0.15, 0.7, 0.15])
                    with col2:
                        st.image(page_img, caption=f"Página {resolve_page} del documento", use_container_width=True)
                        st.markdown(f"[:gray-background[Documento Completo]]({document_url})") 
                else:
                    st.error("No se pudo descargar el archivo PDF.")
    else:
        # Si no hay fuentes, mostrar un mensaje de error
        with st.status("Obteniendo fuentes. Ninguna fuente encontrada."):
            st.write("No se encontraron fuentes relevantes.")
