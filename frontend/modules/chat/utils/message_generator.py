import streamlit as st
import websocket

def message_generator(ws):
    print("[messages_geneator]")
    try:
        while True:
            response = ws.recv()  # Recibe el mensaje del servidor WebSocket
            if response == "FIN":
                break
            yield response  # Devuelve el mensaje recibido como parte del generador
    except Exception as e:
        yield f"Error al recibir el mensaje: {e}"