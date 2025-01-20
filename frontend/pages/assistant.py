import streamlit as st
import ollama
import json
import requests
import websocket
import uuid
from streamlit_feedback import streamlit_feedback
from modules.chat.utils.message_generator import message_generator
from modules.chat.utils.remove_words import remove_word
from modules.chat.visuals.show_chat_component import model_selector, show_sources
from modules.chat.utils.random_placeholder import get_placeholder_manager
from modules.chat.visuals.show_messages import handle_user_input, display_history, get_limited_history, add_message
from modules.settings.utils.load_theme_extra_config import load_theme_extra_config

BACKEND_URL = st.secrets.get("BACKEND_URL", "Not Found")
BACKEND_WS_URL = st.secrets.get("BACKEND_WS_URL", "Not Found")
MODEL_LLM_BASE = st.secrets.get("MODEL_LLM_BASE", "Not Found")
MODEL_EMBEDDING = st.secrets.get("MODEL_EMBEDDING", "Not Found")
MAX_HISTORY_SIZE = st.secrets.get("MAX_HISTORY_SIZE", "Not Found")
NOMBRE_ASISTENTE = st.secrets.get("NOMBRE_ASISTENTE", "Not Found")

theme_extra_config = load_theme_extra_config()

# st.write(st.session_state)
# st.write(1)

st.title(f'Bienvenido a :{theme_extra_config["primary_assistant_color"]}[{NOMBRE_ASISTENTE}]')

if "user_session_uuid" not in st.session_state:
    st.session_state.user_session_uuid = str(uuid.uuid4())
#!!!!!!!!!!! ARREGLAR LOGICA CUANDO SE CAMBIA VARIAS VECES
if "selected_model" not in st.session_state:
    st.session_state.selected_model = MODEL_LLM_BASE
#!!!!!!!!!!!
if "random_placeholder_generated" not in st.session_state:
    random_placeholder = get_placeholder_manager()
    st.session_state.random_placeholder_generated = random_placeholder.get_next_placeholder()
if "history_messages" not in st.session_state:
    st.session_state.history_messages = []
if "use_considerations" not in st.session_state:
    st.session_state.use_considerations = False
if "n_documents" not in st.session_state:
    st.session_state.n_documents = 4
if "word_list" not in st.session_state:
    st.session_state.word_list = []
if "list_interaction_uuid" not in st.session_state:
    st.session_state.list_interaction_uuid = []

on_llm = st.toggle("Seleccionar LLM", help=f"Modelo seleccionado: {st.session_state.selected_model}")
if on_llm:
    model_selector(ollama.list())

on_advance = st.toggle("Configuración avanzada")
if on_advance:
    with st.sidebar:
        on_considerations = st.toggle("Usar Consideraciones")
        if on_considerations:
            st.session_state.use_considerations = True
        else:
            st.session_state.use_considerations = False

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
    st.session_state.use_considerations = False
    st.session_state.n_documents = 4
    st.session_state.word_list = []

st.header("Haga una pregunta sobre el PDF")
placeholder_info = st.empty()
placeholder_error = st.empty()
placeholder_waring = st.empty()
display_history()

# Recibir la entrada del usuario
query = st.chat_input(f"{st.session_state.random_placeholder_generated}")
# st.write(2)

try:
    last_interaction_uuid = st.session_state["list_interaction_uuid"][-1]
    
    if st.session_state.get(last_interaction_uuid):
        # st.write(f"lo consigue y es: {st.session_state.get(last_interaction_uuid)}")

        if isinstance(st.session_state.get(last_interaction_uuid), dict):
            # for key, value in st.session_state.get(last_interaction_uuid).items():
            #     st.write(f"Clave: {key}, Tipo de valor: {type(value), }, Valor: {value}")
            feedback_data = st.session_state.get(last_interaction_uuid)
            # st.write(feedback_data)
            #st.write(type(feedback_data))

            json_data={
                "user_session_uuid": st.session_state.user_session_uuid,
                "interaction_uuid": last_interaction_uuid,
                "feedback_type": feedback_data.get("type", ""),
                "score": feedback_data.get("score", ""),
                "text": feedback_data.get("text", ""),
            }

            # st.write(json_data)
            try:
                response = requests.post(f"{BACKEND_URL}/process_feedback", json=json_data)
            except Exception as e:
                print(f"[assitant] error {e}")
                st.error("Error al conectarse con el servidor...")
    # else:
    #     st.write("no hay nada")
except:
    last_interaction_uuid = None

# Mostrar el valor
# st.write(f"El último interaction_uuid es: {last_interaction_uuid}")
# st.write(f"Type de interaction_uuid es: {type(last_interaction_uuid)}")

if query:
    handle_user_input(query)

    with st.spinner("Buscando información relacionada..."):
        json_data={
            "user_session_uuid": st.session_state.user_session_uuid,
            "query": query,
            "use_considerations": st.session_state.use_considerations,
            "n_documents": st.session_state.n_documents,
            "word_list": st.session_state.word_list,
        }
        response = requests.post(f"{BACKEND_URL}/get_sources", json=json_data)
        # Realizar la consulta al backend

        if response.status_code == 200:
            result = response.json()
            print("[assistant] result: ", result)
            sources = result.get('sources', '')
            print("[assistant] Sources:", sources)
            print("[assistant] Sources type: ", type(sources))
            interaction_uuid = result.get('interaction_uuid', '')
            print("[assistant] Sources:", interaction_uuid)
            print("[assistant] Sources type: ", type(interaction_uuid))
            if sources == "":
                placeholder_info = st.info(":material/info: No se encontraron fuentes relevantes para tu pregunta")
            elif sources:
                show_sources(sources)
        
        # if interaction_uuid not in st.session_state:
        #     print(f"[no encuentra el {interaction_uuid}]")
        # else:
        #     print(f"[encuentra el {interaction_uuid}]")
    
    with st.chat_message("assistant"):
        try:
            # Establecer conexión con el WebSocket
            ws = websocket.create_connection(BACKEND_WS_URL)
            if ws.connected:
                message_data = {
                    "user_session_uuid": st.session_state.user_session_uuid,
                    "interaction_uuid": interaction_uuid,
                    "model_name": st.session_state.selected_model,
                    "history_messages": st.session_state.history_messages,
                }
                # Enviar un mensaje inicial
                ws.send(json.dumps(message_data))

                # # Recibir y mostrar respuestas del WebSocket
                with st.spinner("Generando respuesta..."):
                    full_response = st.write_stream(message_generator(ws))
                    print("[assistant] tipo de full_response: ", type(full_response))

                    add_message("assistant", full_response)
                    
                    json_data={
                        "user_session_uuid": st.session_state.user_session_uuid,
                        "interaction_uuid": interaction_uuid,
                        "full_response": full_response,
                    }
                    
                    requests.post(f"{BACKEND_URL}/add_response", json=json_data)

                    feedback = streamlit_feedback(
                            feedback_type="thumbs",
                            key=f"{interaction_uuid}",
                            align="flex-start",
                        )
                    st.session_state.list_interaction_uuid.append(interaction_uuid)
            else:
                placeholder_waring.warning("WebSocket connection failes")
        except Exception as e:
            placeholder_error.error(f"Failed to establish a WebSocket connection: {e}")
   
    
    
    # st.write(st.session_state)

    # if interaction_uuid not in st.session_state:
    #     print(f"[no encuentra el {interaction_uuid}]")
    # else:
    #     print(f"[encuentra el {interaction_uuid}]")

    # placeholder_waring.warning(st.session_state.history_messages)
# else:
#     placeholder_info.info(":material/info: Por favor, introduce una consulta.")