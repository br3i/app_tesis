
def show_email(email):
    first_part = email.split('@')[0][:3]  # Primeros 3 caracteres antes del "@"
    domain_part = email.split('@')[1]
    domain_suffix = domain_part.split('.')[1]  # El sufijo del dominio (ej. "com")

    # Devolvemos la versión parcial del correo
    return f"{first_part}...@...{domain_suffix}"