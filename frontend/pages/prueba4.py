import streamlit as st
import ollama
from typing import List, Dict, Generator


def ollama_generator(model_name: str, messages: List[Dict[str, str]]) -> Generator:
    print(f"[PRUEBA4.py] llega esto en messager: {messages}")
    print(f"[PRUEBA4.py] tipo: {type(messages)}")
    stream = ollama.chat(model=model_name, messages=messages, stream=True)
    for chunk in stream:
        yield chunk["message"]["content"]


st.title("Ollama with Streamlit demo")
if "selected_model" not in st.session_state:
    st.session_state.selected_model = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

# Obtener la respuesta de ollama.list()
response = ollama.list()
# st.write("Response from ollama.list():", response)  # Imprime la respuesta para ver la estructura

# Acceder a los nombres de los modelos correctamente
if "models" in response:
    st.session_state.selected_model = st.selectbox(
        "Please select the model:", [model.model for model in response["models"]]
    )
else:
    st.error("No models found in the response")

# Mostrar el historial de mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How could I help you?"):
    # Agregar el mensaje del usuario al historial de chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Mostrar el mensaje del usuario en el contenedor de mensajes
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.write_stream(
            ollama_generator(st.session_state.selected_model, st.session_state.messages)
        )
    st.session_state.messages.append({"role": "assistant", "content": response})
