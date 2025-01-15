from datetime import datetime

def convert_datetime(time_str):
    """
    Formatea el campo 'created_at' para mostrar solo la fecha en formato 'YYYY-MM-DD'.
    Acepta el formato 'YYYY-MM-DD HH:MM:SS.ssssss'.
    """
    # Convertir la cadena a datetime (con 'T' entre la fecha y la hora)
    time = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%f")
    
    # Devolver la fecha en formato 'YYYY-MM-DD'
    return time

def convert_to_string(date_obj):
    """
    Convierte un objeto datetime a una cadena en formato 'YYYY-MM-DDTHH:MM:SS.ssssss'.
    """
    # Asegurarse de que el objeto es un datetime
    if isinstance(date_obj, datetime):
        return date_obj.strftime("%Y-%m-%dT%H:%M:%S.%f")
    else:
        raise ValueError("El argumento debe ser un objeto datetime")