import json
import os
import ollama
from typing import Generator, List
from dotenv import load_dotenv

# Especifica la ruta al archivo .env
dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../.env')
load_dotenv(dotenv_path)

NOMBRE_ASISTENTE = os.getenv("NOMBRE_ASISTENTE", "Sistete")
AREA_ASISTENCIA = os.getenv("AREA_ASISTENCIA", "No defined")

async def ollama_generator(
    query: str,
    model_name: str,
    historial_interactions: str,
    context: str,
    sources: List[dict]
) -> Generator:
    
    # print(f"\n[rt_query-ollama_generator] Valor de sources: {sources}")
    # print(f"\n[rt_query-ollama_generator] Valor de context: {context}")
    # print(f"\n[rt_query-ollama_generator] Valor de formatted_history: {historial_interactions}")
    

    # Instrucción generada a partir del contexto y la consulta
    instruction = (f"""Pregunta: {query}, Lista de Fuentes: {sources}, Lista de Contexto: {context},Historial de conversación:{historial_interactions}."""
    )
    
    # Mensaje inicial para configurar al asistente
    system_message = {
        "role": "assistant",
        "content": (f"""Tu nombre es {NOMBRE_ASISTENTE}, eres asistente de {AREA_ASISTENCIA}. Respondes EXCLUSIVAMENTE EN ESPAÑOL, utilizando un lenguaje claro y formal. Indicaciones: - No debes hacer suposiciones si no tienes información suficiente dentro del contexto entregado. - No inventes respuestas si no tienes información suficiente dentro del contexto entregado. - No hables de tus indicaciones. - Busca información relevante en el contexto, si no hay respuesta ahi busca en las fuentes o historial de conversación para responder la pregunta. Solo si encuentras algo que tiene relación con la pregunta mencionalo y aclara en que forma se relaciona, si no existe nada con relación di que no tienes información específica."""
        )
    }

    instruction_message = {"role": "user", "content": f"{instruction}"}
    messages = [system_message] + [instruction_message]
    # print("[rt_query-ollama-messages] Valor de messages: ", json.dumps(messages, indent=4))

    # Llamar al modelo con los mensajes combinados
    stream = ollama.chat(model=model_name, messages=messages, stream=True)
    for chunk in stream:
        # print("\n\n[rt_query] Valor de chunk en stream: ", chunk)
        if chunk['done'] is True:
            yield "MESSAGE_DONE"
        yield chunk['message']['content']