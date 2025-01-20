import re
def formatted_history(history_interactions):
    print("[formatted_history] llega con : ", history_interactions)

    # Filtramos solo los valores 'query' y 'full_response' de cada interacción
    formatted_data = []
    for interaction in history_interactions:
        if interaction.get('full_response') is not None:
            query = interaction.get('query').replace("\n", " ")
            query = re.sub(r'\s{2,}', ' ', query)
            full_response = interaction.get('full_response').replace("\n", " ")
            full_response = re.sub(r'\s{2,}', ' ', full_response)
            formatted_data.append({
                'user': query,
                'assistant': full_response
            })
    
    print("[formatted_history] datos formateados: ", formatted_data)
    return formatted_data


#!!! -> Funciona perfecto
# def formatted_history(history_interactions):
#     print("[formatted_history] llega con : ", history_interactions)

#     # Filtramos solo los valores 'query' y 'full_response' de cada interacción
#     formatted_data = []
#     for interaction in history_interactions:
#         query = interaction.get('query')
#         full_response = interaction.get('full_response')
#         formatted_data.append({
#             'query': query,
#             'full_response': full_response
#         })
    
#     print("[formatted_history] datos formateados: ", formatted_data)
#     return formatted_data



#!!!!!! -> en teroria bien
# def formatted_history(history_interactions, history_messages):
#     # Crear el diccionario a partir de history_interactions
#     interaction_dict = {
#         interaction['interaction_uuid']: {
#             'interaction_uuid': interaction['interaction_uuid'],
#             'query': interaction['query'],
#             'content': next(
#                 (msg['content'] for msg in history_messages if msg.get('interaction_uuid') == interaction['interaction_uuid']),
#                 None
#             )
#         }
#         for interaction in history_interactions
#     }

#     formatted_output = []
#     for idx, (uuid, interaction) in enumerate(interaction_dict.items(), start=1):
#         if interaction['content'] is not None:
#             query = interaction['query']
#             content = interaction['content'] or "Respuesta no disponible"
#             formatted_output.append(f"Interacción {idx}: [user: {query}, assistant: {content}]")

#     return formatted_output



#!!! 2
# def formatted_history(history_interactions, history_messages):
#     # Crear un índice para history_messages basado en interaction_uuid
#     message_dict = {msg['interaction_uuid']: msg['content'] for msg in history_messages if 'interaction_uuid' in msg}

#     # Crear el diccionario de interacciones
#     interaction_dict = {
#         interaction['interaction_uuid']: {
#             'interaction_uuid': interaction['interaction_uuid'],
#             'query': interaction['query'],
#             'content': message_dict.get(interaction['interaction_uuid'], None)
#         }
#         for interaction in history_interactions
#     }

#     # Filtrar y formatear las interacciones
#     formatted_output = [
#         f"Interacción {idx}: [user: {interaction['query']}, assistant: {interaction['content']}]"
#         for idx, interaction in enumerate(interaction_dict.values(), start=1)
#         if interaction['content'] is not None
#     ]

#     return formatted_output

#!!!! 3
# def formatted_history(history_interactions, history_messages):
#     # Crear un índice para history_messages basado en interaction_uuid
#     message_dict = {
#         msg['interaction_uuid']: msg['content']
#         for msg in history_messages if 'interaction_uuid' in msg
#     }

#     # Crear el diccionario de interacciones
#     interaction_dict = {
#         interaction['interaction_uuid']: {
#             'interaction_uuid': interaction['interaction_uuid'],
#             'query': interaction['query'],
#             'content': message_dict.get(interaction['interaction_uuid'], None)
#         }
#         for interaction in history_interactions
#     }

#     # Filtrar y formatear las interacciones
#     formatted_output = [
#         f"Interacción {idx}: [user: {interaction['query']}, assistant: {interaction['content']}]"
#         for idx, interaction in enumerate(interaction_dict.values(), start=1)
#         if interaction['content'] is not None  # Excluir interacciones sin respuesta
#     ]

#     return formatted_output