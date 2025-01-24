import re


# Función para validar criterios de la contraseña
def validate_password(password: str):
    """
    Valida la contraseña utilizando un patrón dinámico.
    Devuelve los criterios y un valor booleano que indica si cada criterio se cumple.
    """
    # Definir el patrón para la validación dentro de la función
    special_characters = "@$!%*?&"

    # Validar los criterios
    criteria = {
        "Debe tener entre 8 y 20 caracteres": 8 <= len(password) <= 20,
        "Debe contener al menos una letra mayúscula": bool(
            re.search(r"[A-Z]", password)
        ),
        "Debe contener al menos una letra minúscula": bool(
            re.search(r"[a-z]", password)
        ),
        "Debe contener al menos un número": bool(re.search(r"\d", password)),
        f"Debe contener al menos un carácter especial de los siguientes: {special_characters}": bool(
            re.search(r"[@$!%*?&]", password)
        ),
    }

    # Validar si todos los criterios son cumplidos
    all_criteria_met = all(criteria.values())

    return all_criteria_met, criteria
