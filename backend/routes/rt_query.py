
#!!!!!!! SI hay error descomentar todo 
# routes/routes_query.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from services.documents.obtain_docs.context_sources_service import get_context_sources
# from query_service

router = APIRouter()

# Definir el modelo para la consulta
class QueryModel(BaseModel):
    query: str
    word_list: List[str]
    n_documents: int

@router.post("/get_context_sources")
async def context_sources(query_model: QueryModel):
    print("[rt_query] queryl: ", query_model.query)
    print("[rt_query] word_list: ", query_model.word_list)
    print("[rt_query] n_documents: ", query_model.n_documents)

    query = query_model.query
    word_list = query_model.word_list
    n_documents = query_model.n_documents
    response = get_context_sources(query, word_list, n_documents)
    print("\n\n-----------------------VERIFICAR CONTEXTO----------------")
    print(response)
    print("\n\n\n\n")
    return response

# @router.post("/ai")
# async def ai_post(query_model: QueryModel):
#     query = query_model.query
#     response = query_service.query_with_gemini(query)
#     return response
