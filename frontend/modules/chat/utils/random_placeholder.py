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
                self.weights[i] = 0
            else:
                self.weights[i] = 1

    def get_next_placeholder(self):
        self.adjust_weights()
        chosen_index = random.choices(
            range(len(self.placeholders)), weights=self.weights, k=1
        )[0]
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
    "¿Te gustaría encontrar información académica? 📚",
]


# Función para obtener una instancia de PlaceholderWithWeights
def get_placeholder_manager():
    return PlaceholderWithWeights(PLACEHOLDER_LIST)
