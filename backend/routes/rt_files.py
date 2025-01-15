
#!!! SI HAY ERROR DESCOMENTAR TODO
# # routes/routes_files.py
# import os
# from urllib.parse import unquote
# from fastapi import APIRouter, UploadFile, File, HTTPException
# from fastapi.responses import FileResponse
# from services import upload_service
# from dotenv import load_dotenv

# # Especifica la ruta al archivo .env
# dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../.env')
# load_dotenv(dotenv_path)

# # Variables de entorno para PostgreSQL
# DOCUMENTS_PATH = os.getenv("DOCUMENTS_PATH")

# router = APIRouter()

# @router.get("/files")
# async def get_files():
#     files = upload_service.get_files()
#     files_data = [{"filename": file} for file in files]
#     return files_data






# @router.delete("/files/{filename}")
# async def delete_file(filename: str):
#     success = upload_service.delete_file(filename)
#     if success:
#         return {"status": f"Archivo {filename} eliminado correctamente."}
#     else:
#         raise HTTPException(status_code=404, detail="Archivo no encontrado")

# @router.put("/files/{filename}")
# async def update_file(filename: str, file: UploadFile = File(...)):
#     file_path = os.path.join("./pdf", filename)

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
