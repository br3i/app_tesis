import json

def treat_context_sources(response_context_sources, use_considerations):
    print("[response_context_sources]")
    response_context_sources = response_context_sources
    context = response_context_sources.get('context', '')
    sources = response_context_sources.get('sources', [])
    # print("[response_context_sources] Context:", context)
    # print("[response_context_sources] Context type: ", type(context))
    # print("[response_context_sources] Sources:", sources)
    # print("[response_context_sources] Sources type: ", type(sources))
    
    if sources == "":
        original_sources = ""
        sources_to_send = ":material/info: No se encontraron fuentes relevantes para tu pregunta"
    else:
        sources_to_send = sources.copy()

    # Si use_considerations es False, eliminamos 'considerations' de los elementos de sources
    if use_considerations == False:
        for item in sources:
            if 'considerations' in item:
                del item['considerations']
        
    return {"context_to_send": context, "sources_to_send": sources_to_send}