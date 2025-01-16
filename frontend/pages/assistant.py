import streamlit as st
import ollama
import json
import requests
from modules.chat.utils.ollama_generator import ollama_generator
from modules.chat.utils.remove_words import remove_word
from modules.chat.visuals.show_chat_component import model_selector, show_sources
from modules.chat.visuals.show_messages import handle_user_input, display_history, get_limited_history, add_message
from modules.settings.utils.load_theme_extra_config import load_theme_extra_config

BACKEND_URL = st.secrets.get("BACKEND_URL", "Not Found")
MODEL_LLM_BASE = st.secrets.get("MODEL_LLM_BASE", "Not Found")
MODEL_EMBEDDING = st.secrets.get("MODEL_EMBEDDING", "Not Found")
MAX_HISTORY_SIZE = st.secrets.get("MAX_HISTORY_SIZE", "Not Found")
NOMBRE_ASISTENTE = st.secrets.get("NOMBRE_ASISTENTE", "Not Found")

theme_extra_config = load_theme_extra_config()

st.title(f'Bienvenido a :{theme_extra_config["primary_assistant_color"]}[{NOMBRE_ASISTENTE}]')

if "selected_model" not in st.session_state:
    st.session_state.selected_model = MODEL_LLM_BASE
if "use_consideratons" not in st.session_state:
    st.session_state.use_consideratons = False
if "history_messages" not in st.session_state:
    st.session_state.history_messages = []
if "use_history" not in st.session_state:
    st.session_state.use_history = False
if "n_documents" not in st.session_state:
    st.session_state.n_documents = 4
if "word_list" not in st.session_state:
    st.session_state.word_list = []

on_llm = st.toggle("Seleccionar LLM")
if on_llm:
    model_selector(ollama.list())

on_advance = st.toggle("Configuración avanzada")
if on_advance:
    with st.sidebar:
        on_considerations = st.toggle("Usar Consideraciones")
        if on_considerations:
            st.session_state.use_consideratons = True
        else:
            st.session_state.use_consideratons = False
        
        on_history = st.toggle("Usar historial")
        if on_history:
            st.session_state.use_history = True
        else:
            st.session_state.use_history = False

        on_n_docs = st.toggle("Numero de documentos")
        if on_n_docs:
            n_docs = st.number_input("Ingrese el número de documentos", min_value=4, max_value=10, value="min", step=1, key="n_docs", help="Cantidad de documentos que desea como fuentes", placeholder="N° Documentos", label_visibility="visible")
            st.session_state.n_documents = n_docs
        else:
            st.session_state.n_documents = 4

        on_key_words = st.toggle("Palabras Clave")
        if on_key_words:
            with st.form(key='add_word_form', border=False):
                word_input = st.text_input('Ingrese una palabra clave', value="", placeholder='ej. Resolución')
                submit_button = st.form_submit_button('Añadir')

                if submit_button and word_input != "":
                    if word_input != "" and word_input not in st.session_state.word_list:
                        st.session_state.word_list.append(word_input)
                    elif word_input in st.session_state.word_list:
                        st.warning("La palabra ya existe. Ingresa una palabra diferente.")
            if st.button('Limpiar lista'):
                st.session_state.word_list = []

            st.write("Lista de Palabras Clave:")
            for word in st.session_state.word_list:
                with st.container(border=True):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                            st.html(f"""
                                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                                        <p style='padding: 10px; margin: 0;'>{word}</p>
                                    </div>
                                    """
                            )
                    with col2:
                        if st.button(f"", key=word, on_click=remove_word, args=(word,), icon=":material/close:"):
                            pass
        else:
            st.session_state.word_list = []
else:
    st.session_state.use_consideratons = False
    st.session_state.use_history = False
    st.session_state.n_documents = 4
    st.session_state.word_list = []

st.header("Haga una pregunta sobre el PDF")
placeholder_info = st.empty()
placeholder_waring = st.empty()
display_history()

# Recibir la entrada del usuario
query = st.chat_input("Introduce tu consulta sobre el documento PDF")

if query:
    handle_user_input(query)

    with st.spinner("Buscando información relacionada..."):
        json_data={
            "query": query,
            "word_list": st.session_state.word_list,
            "n_documents": st.session_state.n_documents
        }
        response = requests.post(f"{BACKEND_URL}/get_context_sources", json=json_data)
        # Realizar la consulta al backend

        if response.status_code == 200:
            result = response.json()
            print("[assistant] result: ", result)
            context = result.get('context', '')
            sources = result.get('sources', '')
            print("[assistant] Context:", context)
            print("[assistant] Context type: ", type(context))
            print("[assistant] Sources:", sources)
            print("[assistant] Sources type: ", type(sources))
            if sources == "":
                original_sources = ""
                placeholder_info = st.info(":material/info: No se encontraron fuentes relevantes para tu pregunta")
            else:
                original_sources = sources.copy()

            # Si use_consideratons es False, eliminamos 'considerations' de los elementos de sources
            if st.session_state.use_consideratons == False:
                for item in sources:
                    if 'considerations' in item:
                        del item['considerations']

            if sources:
                show_sources(original_sources)
                

    # Limitar el historial para la generación del modelo
    limited_history = get_limited_history(MAX_HISTORY_SIZE)

    # Determinamos qué versión de 'sources' enviar a ollama_generator
    if st.session_state.use_consideratons:
        sources_to_send = original_sources  # Enviamos la versión original si 'use_consideratons' es True
    else:
        sources_to_send = sources
    
    if st.session_state.use_history:
        history_to_send = limited_history
    else:
        history_to_send = ["Historial no disponible"]

    # Llamar a la función de generación con el historial limitado
    with st.chat_message("assistant"):
        print("\n\n------------ULTIMA VEZ DE CONTEXTO---------------")
        print(context)
        print("\n\n\n\n")
        message_placeholder = st.empty()  # Crear placeholder DENTRO del chat_message
        full_response = ""
        with st.spinner("Generando respuesta..."): #Spinner opcional
            for chunk in ollama_generator(
                st.session_state.selected_model,
                history_to_send,
                query,
                context,
                sources_to_send
            ):
                full_response += chunk
                message_placeholder.markdown(full_response + " ▌")

        message_placeholder.markdown(full_response)
    add_message("assistant", full_response)

else:
    placeholder_info.info(":material/info: Por favor, introduce una consulta.")