# modules/chat_utils.py
import streamlit as st


# Función para agregar un mensaje al historial
def add_message(role, content):
    st.session_state.history_messages.append({"role": role, "content": content})


# Función para mostrar el historial de mensajes
def display_history():
    for message in st.session_state.history_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# Función para manejar la entrada del usuario
def handle_user_input(query):
    if query:
        add_message("user", query)
        with st.chat_message("user"):
            st.markdown(query)
    else:
        st.warning("Por favor, introduce una consulta.")
