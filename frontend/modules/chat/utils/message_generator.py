import streamlit as st
import websocket
import json

def message_generator(ws):
    print("[message_generator] Iniciando...")
    try:
        while True:
            # Recibir mensaje del WebSocket
            response = json.loads(ws.recv())
            print(f"[message_generator] response: {response}")

            # Detener el generador al encontrar "MESSAGE_DONE"
            if response.get("content") == "MESSAGE_DONE":
                break

            # Devuelve solo el contenido válido (si existe)
            content = response.get("content", "")
            if content:
                yield content

    except Exception as e:
        yield {"error": f"Error al recibir el mensaje: {e}"}