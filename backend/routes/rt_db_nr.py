from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from services.nr_database.nr_connection_service import get_collection_names
#!!!!!! APLICAR PARA GEMINI
#import services.query_service

router = APIRouter()

class QueryModel(BaseModel):
    query: str

@router.get("/collection_names")
async def rt_get_collection_names():
    # Lógica para obtener las colecciones desde tu base de datos
    collection_names = get_collection_names()
    print("Las colecciones que se obtienen de la base: ", collection_names)
    return JSONResponse(content={"collections": collection_names})

# @router.post("/ai")
# async def ai_post(query_model: QueryModel):
#     query = query_model.query
#     response = query_service.query_with_gemini(query)
#     return response
