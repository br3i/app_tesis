import os
import time
import numpy as np
from services.helpers.return_collection import return_collection
from services.helpers.extract_resolution_info import extract_resolution_info
from services.nr_database.nr_connection_service import get_collection_names
from services.embeddings.get_embedding_service import get_embeddings

def get_context_sources(query: str, word_list, n_documents):
    # print(f"\n\n--------------[contex_sources_service] Iniciando búsqueda con query: {query}")
    # print(f"[context_sources_service] Número de documentos a buscar: {n_documents}")
    # print(f"[context_sources_service] n_documents type: {type(n_documents)}")
    n_documents = int(n_documents)
    # print(f"[context_sources_service] n_documents type: {type(n_documents)}")
    # print(f"[context_sources_service] word_list type: {type(word_list)}")
    # print(f"[context_sources_service] word_list: {word_list}")

    try:
        # Obtener colecciones disponibles
        collection_names = get_collection_names()
        print(f"Valor de colecction names que se obtiene: {collection_names}")
        if not collection_names:
            return {"error": "No se encontraron colecciones en la base de datos."}

        # Generar embedding para la consulta
        query_embedding = get_embeddings(query)
        #print(f"[QUERY_PDF] Embedding generado para la consulta: {query_embedding}")

        # Buscar documentos relevantes en todas las colecciones
        all_documents = []
        sources = []
        metadata_filters = {}
        full_text_filters = {}

        year, resolution = extract_resolution_info(query)
        
        # print(f"[CONTEX-SOURCES-SERVICE] Word_list to Contain: {word_list}")
        # print("[CONTEX-SOURCES-SERVICE] Resolución y año extraídos: ", year, resolution)

        # Si ambos año y resolución están presentes, usar $or
        if year and resolution:
            metadata_filters = {
                "$or": [
                    {
                        "collection_name": {"$eq": str(year)}
                    },
                    {
                        "collection_name": {"$eq": str(resolution)}
                    }
                ]
            }
        elif year:
            metadata_filters = {
                "collection_name": {"$eq": str(year)}
            }
        elif resolution:
            metadata_filters = {
                "number_resolution": {"$eq": str(resolution)}
            }

        # print("[CONTEXT-SOURCES-SERVICE] Filtros de metadata: ", metadata_filters)
        # print("[CONTEXT-SOURCES-SERVICE] Lend word_list: ", len(word_list))
        
        if len(word_list) != 0:
            if len(word_list) > 2:
                full_text_filters = {
                    "$or": [{"$contains": word} for word in word_list]
                }
            else:
                full_text_filters = {"$contains": " ".join(word_list)}
        else:
            full_text_filters = {}

        # print("[CONTEXT-SOURCES-SERVICE] filtros de where_documents: ", full_text_filters)

        for collection_name in collection_names:
            print(f"[contex_sources_service] Buscando en colección: {collection_name}")
            collection = return_collection(collection_name)
            
            search_results = collection.query(
                query_embeddings=[query_embedding],
                n_results=n_documents,
                where=metadata_filters,
                where_document=full_text_filters,
                include=["documents", "metadatas"]
            )
            # print(f"\nRESULTS\n\n------[contex_sources_service] Resultado de search_results {search_results}")
            
            # Verificar si 'documents' contiene resultados y procesarlos
            if 'documents' in search_results and search_results['documents']:
                # Obtener los documentos de 'documents'
                documents = search_results['documents'][0]  # Acceder al primer conjunto de documentos
                # print("\n\n\n CONSEGUIR DOCUMENTS: \n", documents)
                metadatas = search_results['metadatas'][0]  # Obtener los metadatos correspondientes
                # print("\n\n\n CONSEGUIR METADATAS: \n", metadatas)
                
                # print(f"----\nDocumentos\n\n[contex_sources_service] Documentos encontrados en {collection_name}: {documents}")
                
                # Almacenar los textos de los documentos encontrados y las fuentes
                for i, doc in enumerate(documents):
                    if doc:  # Verificar que el documento no sea None o vacío
                        all_documents.append(doc)  # Agregar el texto del documento a la lista all_documents

                        considerations = metadatas[i]['considerations']
                        # print(f"\n\n\n CONSEGUIR CONSIDERATIONS de {i}: \n", considerations)
                        resolve_page = metadatas[i]['resolve_page']
                        # print(f"\n\n\n CONSEGUIR resolve_page de {i}: \n", resolve_page)
                        file_path = metadatas[i]['file_path']
                        # print(f"\n\n\n CONSEGUIR FILE_PATH de {i}: \n", file_path)
                        document_name = metadatas[i]['document_name']
                        # print(f"\n\n\n CONSEGUIR document_name de {i}: \n", document_name)

                        # Agregar la fuente (documento y página) a la lista de fuentes
                        document_metadata = metadatas[i]
                        
                        sources.append({
                            'file_path' : file_path,
                            #'document_name': os.path.splitext(document_metadata['document_name'])[0],
                            'document_name': document_name,
                            'considerations': considerations,
                            'resolve_page': resolve_page
                        })
                    else:
                        print(f"[contex_sources_service] El documento está vacío o es None")

            else:
                print(f"\n\n-----[contex_sources_service] No se encontraron documentos en la colección {collection_name}")

        # Verificar si se encontraron documentos válidos
        if not all_documents:
            return {"error": "No se encontraron documentos relevantes en las colecciones."}

        # Generar contexto combinado
        context = "\n".join(all_documents)
        # print("\n\n----------------------CONTEXTO--------------------")
        # print(f"[contex_sources_service] all_documents combinado: {context}\n\n\n\n")

        return {"context": context,"sources": sources}

    except Exception as e:
        print(f"[contex_sources_service] Error al procesar la consulta: {str(e)}")
        return {"error": f"Error al procesar la consulta: {str(e)}"}
