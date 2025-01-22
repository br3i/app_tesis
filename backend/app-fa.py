# import os
# import json
# from fastapi import FastAPI, File, Form, UploadFile, HTTPException
# from fastapi import WebSocket, WebSocketDisconnect
# from fastapi.responses import FileResponse, JSONResponse
# from pydantic import BaseModel
# from dotenv import load_dotenv
# from sqlalchemy.orm import Session
# from models import init_db, database
# import services.upload_service
# import services.process_documents_service
# import services.embedding_service
# import services.save_embedding_service
# import services.search_service
# import services.query_service
# import services.query_service2
# import services.database_conection_service


# load_dotenv()

# # Inicializa FastAPI
# app = FastAPI()

# # Inicializar la base de datos
# init_db()

# # Inyección de la sesión en las rutas
# def get_db():
#     db = database.SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# # Configura la clave de API de Gemini
# api_key = os.getenv("GEMINI_API_KEY")
# if not api_key:
#     raise Exception(
#         "Por favor, configura la clave API de Google Gemini en el archivo .env."
#     )

# # Configura la ruta de almacenamiento de archivos
# UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "pdf")
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# app.config = {"UPLOAD_FOLDER": UPLOAD_FOLDER}

# # Definir el modelo para la consulta
# class QueryModel(BaseModel):
#     query: str

# @app.websocket('/ws')
# async def websocket_endpoint(websocket: WebSocket):
#     print("WebSocket connection established.")
#     await websocket.accept()

#     try:
#         while True:
#             # Recibiendo el mensaje del cliente (Streamlit)
#             data = await websocket.receive_text()
#             print("Received data from client:", data)
#             data_dict = json.loads(data)
#             print("Parsed data:", data_dict)

#             user_message = data_dict["query"]  # Ahora el JSON del cliente tendrá 'query' como la clave
#             print("User message:", user_message)

#             addPrompt = f"El usuario dice: {user_message}. Responde UNICAMENTE en español y Limita tu respuesta a 300 palabras."
#             print("Formatted prompt for model:", addPrompt)

#             # Fetching context from Chroma (asegúrate de que la función `chroma.get_context_from_query` esté bien implementada)
#             print("Fetching context from Chroma...")
#             context = chroma.get_context_from_query(query_text=user_message, n_results=10)
#             print("Context fetched from Chroma:", context)

#             # Callback para manejar el contenido generado por el modelo
#             async def completion_callback(chunk):
#                 print("Callback chunk received:", chunk.choices[0].delta.content)
#                 message = {"event": "chunk", "content": chunk.choices[0].delta.content}
#                 await websocket.send_text(json.dumps(message))  # Enviar el fragmento al cliente
#                 print("Sent chunk message to client:", message)

#             # Callback al finalizar el procesamiento
#             async def finish_completion_callback():
#                 message = {"event": "finish", "content": ""}
#                 await websocket.send_text(json.dumps(message))  # Enviar el mensaje de fin al cliente
#                 print("Sent finish message to client:", message)

#             print("Generating completion...")
#             # Generación de la respuesta utilizando la función de completado
#             await create_completion_generator(addPrompt, get_system_prompt(context), completion_callback)
#             await finish_completion_callback()

#     except Exception as e:
#         print(f"Error: {e}")


# @app.post("/collection_names")
# async def get_collection_names():
#     # Lógica para obtener las colecciones desde tu base de datos
#     collection_names = services.database_conection_service.get_collection_names()
#     print("Las colecciones que se obtienen de la base: ", collection_names)
#     return JSONResponse(content={"collections": collection_names})


# @app.post("/ai")
# async def ai_post(query_model: QueryModel):
#     query = query_model.query
#     response = query_service.query_with_gemini(query)
#     return response

# @app.get("/pdf/{filename}")
# async def serve_pdf(filename: str):
#     pdf_directory = "./pdf"  # Asegúrate de que esta ruta sea correcta
#     file_path = os.path.join(pdf_directory, filename)

#     if os.path.exists(file_path):
#         print(f"Ruta del archivo: {file_path}")
#         return FileResponse(file_path)
#     else:
#         raise HTTPException(status_code=404, detail="Archivo no encontrado")

# @app.post("/pdf")
# async def pdf_post(collection_name: str = Form(...), file: UploadFile = File(...)):
#      # Verificar los datos recibidos
#     print(f"Datos recibidos: collection_name={collection_name}, file={file.filename}")

#     # Mostrar el nombre del archivo antes de guardarlo
#     print(f"Archivo recibido: {file.filename}")

#     # Identificador único del documento (podría ser el nombre del archivo o algún otro identificador)
#     document_id = os.path.splitext(file.filename)[0]

#     # Verificar si el documento ya existe en la base de datos de embeddings
#     exists = services.upload_service.check_document_exists(document_id, collection_name)

#     if exists:
#         # Si el documento ya existe, respondemos que no es necesario guardarlo
#         response = {
#             "status": "Document already exists",
#             "filename": file.filename,
#             "message": "Este documento ya está registrado en la base de datos."
#         }
#         print(f"Respuesta: {response}")
#         return response

#     # Si el documento no existe, guardamos el archivo
#     file_path = services.upload_service.save_file(file)
#     print(f"Archivo guardado en: {file_path}")

#     # Procesar el PDF y generar embeddings
#     doc_len, chunk_len = services.process_documents_service.process_pdf(file_path, collection_name)

#     # Imprimir la cantidad de documentos y fragmentos procesados
#     print(f"Cantidad de documentos procesados: {doc_len}")
#     print(f"Cantidad de fragmentos procesados: {chunk_len}")

#     response = {
#         "status": "Successfully Uploaded",
#         "filename": file.filename,
#         "doc_len": doc_len,
#         "chunks": chunk_len,
#     }

#     # Imprimir la respuesta antes de devolverla
#     print(f"Respuesta: {response}")

#     return response


# @app.post("/ask_pdf")
# async def ask_pdf_post(query_model: QueryModel):
#     query = query_model.query
#     print("Esto llega desde el frontend en /ask_pdf: ", query)
#     response = services.query_service2.query_pdf(query)
#     # # Guardar la respuesta en un archivo txt
#     # try:
#     #     with open("respuesta_query.txt", "w", encoding="utf-8") as file:
#     #         file.write(str(response))  # Convierte la respuesta a cadena antes de escribirla
#     #     print("Respuesta guardada en 'respuesta_query.txt'")

#     # except Exception as e:
#     #     print(f"Error al guardar la respuesta en el archivo: {e}")

#     # print("Llega a este punto final")
#     return response

# # Ruta para obtener la lista de archivos
# @app.get("/files")
# async def get_files():
#     files = upload_service.get_files()
#     files_data = [{"filename": file} for file in files]
#     return files_data

# # Ruta para obtener el contenido de un archivo
# @app.get("/files/{filename}")
# async def get_file(filename: str):
#     content = upload_service.get_file_content(filename)
#     if content:
#         return content
#     else:
#         raise HTTPException(status_code=404, detail="Archivo no encontrado")

# # Ruta para eliminar un archivo
# @app.delete("/files/{filename}")
# async def delete_file(filename: str):
#     success = upload_service.delete_file(filename)
#     if success:
#         return {"status": f"Archivo {filename} eliminado correctamente."}
#     else:
#         raise HTTPException(status_code=404, detail="Archivo no encontrado")

# # Ruta para actualizar un archivo
# @app.put("/files/{filename}")
# async def update_file(filename: str, file: UploadFile = File(...)):
#     file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

#     # Verificar si el archivo existe
#     if not os.path.exists(file_path):
#         raise HTTPException(status_code=404, detail="Archivo no encontrado")

#     # Eliminar el archivo antiguo
#     os.remove(file_path)

#     # Guardar el nuevo archivo
#     new_file_path = upload_service.save_file(file)
#     doc_len, chunk_len = embedding_service.process_pdf(new_file_path)

#     response = {
#         "status": "Archivo actualizado correctamente",
#         "filename": filename,
#         "new_filename": file.filename,
#         "doc_len": doc_len,
#         "chunks": chunk_len,
#     }
#     return response

# # Ruta para visualizar el archivo PDF
# @app.get("/pdf/{filename}")
# async def serve_pdf(filename: str):
#     pdf_directory = "./pdf"  # Asegúrate de que esta ruta sea correcta
#     file_path = os.path.join(pdf_directory, filename)

#     if os.path.exists(file_path):
#         print(f"Ruta del archivo: {file_path}")
#         return FileResponse(file_path)
#     else:
#         raise HTTPException(status_code=404, detail="Archivo no encontrado")

# # Ejecutar el servidor con Uvicorn
# # Para ejecutar el servidor, usa el siguiente comando:
# # uvicorn app-fa:app --reload --host 0.0.0.0 --port 8080
#!!!!! -> 4 instancias = uvicorn app-fa:app --reload --host 0.0.0.0 --port 8080 --workers 4


# app-fa.py
import time
import os
import json
import ollama
from ollama import chat
from fastapi import FastAPI
from fastapi import WebSocket, WebSocketDisconnect
from routes.rt_code import router as code_router
from routes.rt_db_nr import router as db_nr_router
from routes.rt_documents import router as documents_router
from routes.rt_notification import router as notification_router
from routes.rt_query import router as query_router
from routes.rt_requested_document import router as requested_document_router
from routes.rt_user import router as user_router
from models import init_db
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Inicializa FastAPI
app = FastAPI()

# Inicializar la base de datos
reset_db = (
    os.getenv("RESET_DB", "false").lower() == "true"
)  # Leer de las variables de entorno
init_db(reset=reset_db)

# Incluir las rutas
app.include_router(code_router)
app.include_router(db_nr_router)
app.include_router(documents_router)
app.include_router(notification_router)
app.include_router(query_router)
app.include_router(requested_document_router)
app.include_router(user_router)

# Puedes seguir añadiendo más routers de acuerdo a la organización de tus rutas
