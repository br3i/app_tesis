import random

class PlaceholderWithWeights:
    def __init__(self, placeholders):
        self.placeholders = placeholders
        self.history = []  # Para registrar qué elementos han sido seleccionados
        self.weights = [1] * len(placeholders)  # Peso inicial uniforme

    def adjust_weights(self):
        # Ajustar los pesos basados en la frecuencia de uso (o cualquier otro criterio)
        for i, _ in enumerate(self.placeholders):
            # Si el placeholder ha sido usado recientemente, reducir su peso
            if self.placeholders[i] in self.history[-3:]:  # Por ejemplo, los últimos 3
                self.weights[i] = 0.5
            else:
                self.weights[i] = 1.0

    def get_next_placeholder(self):
        self.adjust_weights()
        chosen_index = random.choices(range(len(self.placeholders)), weights=self.weights, k=1)[0]
        self.history.append(self.placeholders[chosen_index])
        
        # Limitar el tamaño del historial para evitar acumulaciones largas
        if len(self.history) > 10:
            self.history.pop(0)
        
        return self.placeholders[chosen_index]

# Lista de placeholders que quieres tener aquí, no en el archivo principal
PLACEHOLDER_LIST = [
    "¿En qué puedo ayudarte hoy? 😊",
    "¿Qué información necesitas encontrar?",
    "Escribe lo que buscas aquí...",
    "¿Qué estás buscando en los documentos? 📖",
    "Encuentra lo que necesitas fácilmente...",
    "Cuéntame qué necesitas saber...",
    "¿Cómo puedo ayudarte con los archivos?",
    "Busca algo en los documentos de la ESPOCH 🦙",
    "¿Qué tema quieres explorar hoy? 🔎",
    "Dime qué estás buscando...",
    "¿Te gustaría encontrar algo específico? 📑",
    "Escribe aquí lo que necesitas consultar...",
    "¿Qué te gustaría saber sobre los documentos?",
    "Encuentra lo que necesitas rápidamente...",
    "¿Qué resolución te gustaría consultar?",
    "Busca tu documento en segundos ⏳",
    "¿Qué información te gustaría ver hoy?",
    "Escribe tu consulta y te ayudaré...",
    "¿Qué detalles estás buscando?",
    "Cuéntame qué documento necesitas...",
    "Escribe lo que necesitas encontrar aquí...",
    "¿Hay algo específico que quieras consultar?",
    "Encuentra la documentación que necesitas...",
    "¿Cómo puedo ayudarte a encontrar algo?",
    "Escribe para buscar lo que necesitas...",
    "¿Qué documento o tema necesitas hoy? 📂",
    "Dime qué documento estás buscando...",
    "Busca algo relacionado con normativas...",
    "¿En qué puedo asistirte hoy con la documentación?",
    "¿Te gustaría encontrar información académica? 📚"
]

# Función para obtener una instancia de PlaceholderWithWeights
def get_placeholder_manager():
    return PlaceholderWithWeights(PLACEHOLDER_LIST)



# import random

# def random_placeholder():
#     placeholders = [
#         "Escribe una consulta sobre documentación aquí...",
#         "¿Qué necesitas buscar en los archivos?",
#         "Ingresa una palabra clave o frase relevante...",
#         "Encuentra la información que buscas...",
#         "Consulta documentos específicos aquí...",
#         "Escribe tu pregunta sobre los archivos de la ESPOCH...",
#         "¿Qué tema deseas explorar en la documentación?",
#         "Encuentra la resolución que necesitas...",
#         "Escribe el título o palabra clave del documento...",
#         "¿Qué normativa necesitas consultar hoy?",
#         "Busca en los registros de Secretaría General...",
#         "Ingresa detalles para localizar tu documento...",
#         "¿Qué deseas saber sobre los procesos actuales?",
#         "Consulta aquí sobre ajustes curriculares...",
#         "Escribe tu pregunta sobre gestiones académicas...",
#         "Encuentra documentos relevantes rápidamente...",
#         "Introduce un término para empezar tu búsqueda...",
#         "¿Qué resolución estás buscando?",
#         "Consulta documentos oficiales aquí...",
#         "Ingresa una consulta sobre políticas académicas...",
#         "¿Qué necesitas saber de los documentos?",
#         "Escribe para buscar información específica...",
#         "Localiza documentos clave al instante...",
#         "Ingresa el tema que quieres consultar...",
#         "¿Qué procesos de documentación te interesan?",
#         "Busca archivos relacionados con normativas...",
#         "¿Qué detalles necesitas obtener hoy?",
#         "Explora documentación oficial aquí...",
#         "Introduce una palabra clave para tu consulta...",
#         "Empieza tu búsqueda sobre archivos académicos..."
#     ]
#     return random.choice(placeholders)
