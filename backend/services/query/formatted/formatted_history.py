import re
def formatted_history(history_interactions):
    # print("[formatted_history] llega con : ", history_interactions)

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
    
    # print("[formatted_history] datos formateados: ", formatted_data)
    return formatted_data