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
            print(f"[message_generator] tipo response: {type(response)}")

            # Detener el generador al encontrar "MESSAGE_DONE"
            if isinstance(response.get("content"), dict) and response["content"].get("key") == "MESSAGE_DONE":
                st.session_state.ollama_times = {
                    "created_at": response["content"].get("created_at"),
                    "total_duration": response["content"].get("total_duration"),
                    "load_duration": response["content"].get("load_duration"),
                    "prompt_eval_count": response["content"].get("prompt_eval_count"),
                    "prompt_eval_duration": response["content"].get("prompt_eval_duration"),
                    "eval_count": response["content"].get("eval_count"),
                    "eval_duration": response["content"].get("eval_duration"),
                }
                break

            # Devuelve solo el contenido válido (si existe)
            content = response.get("content", "")
            if content:
                yield content

    except Exception as e:
        yield {"error": f"Error al recibir el mensaje: {e}"}