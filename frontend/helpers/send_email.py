# Brevo => pip install git+https://github.com/sendinblue/APIv3-python-library.git
from __future__ import print_function
import streamlit as st
import sib_api_v3_sdk
import requests
import json
from datetime import datetime
from sib_api_v3_sdk.rest import ApiException
from helpers.create_code import create_code

# Cargar configuraciones desde secretos
BACKEND_URL = st.secrets.get("BACKEND_URL", "Not Found")
API_BREVO = st.secrets.get("API_BREVO", "Not Found")
NOMBRE_ASISTENTE = st.secrets.get("NOMBRE_ASISTENTE", "Not Found")
EMAIL_SENDER = st.secrets.get("EMAIL_SENDER", "Not Found")
code = create_code()

# Configuración de la API de Brevo
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = API_BREVO

def get_subject(email_type):
    """Obtener el asunto del correo basado en el tipo de correo."""
    subject_map = {
        'password_recovery': "Recuperación de Contraseña",
        'username_recovery': "Recuperación de Nombre de Usuario",
        'email_verification': "Verificación de Correo Electrónico",
        # Agrega más tipos de correo aquí si es necesario
    }
    return subject_map.get(email_type, "Error: El tipo de correo no es válido.")


def generate_email_content(email_type, username=None, code=None):
    año_actual = datetime.now().year
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Correo Electrónico</title>
        <style>
            body {{
                font-family: sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f0f0f5; /* Lila muy claro de fondo */
            }}
            .container {{
                max-width: 600px;
                margin: 20px auto;
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                border: 2px solid #9370db; /*Borde morado*/
            }}
            header {{
                background-color: #9370db; /* Morado del header */
                color: white;
                padding: 20px;
                text-align: center;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }}
            h1 {{
                margin: 0;
                font-size: 24px;
            }}
            .content {{
                padding: 20px;
                color: #333;
            }}
            .code {{
                font-size: 24px;
                font-weight: bold;
                text-align: center;
                margin: 20px 0;
                background-color: #f8f8f8; /* Fondo gris claro para el código */
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #ddd;
            }}
            .footer {{
                background-color: #f8f9fa;
                text-align: center;
                padding: 10px;
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
                font-size: 14px;
                color: #555;
            }}
            .highlight {{
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>
    """

    match email_type:
        case 'password_recovery':
            html_content += "Código de Verificación</h1></header>"
            html_content += f"""
                <div class="content">
                    <p>Estimado usuario <span class="highlight">{username}</span>,</p>
                    <p>Este es su código de verificación: </p>
                    <div class="code">{code}</div>
                    <p>Recuerde que este código estará disponible por <span class="highlight">15 minutos</span>. Si no lo ha solicitado, por favor ignore este mensaje.</p>
                </div>"""
        case 'username_recovery':
            html_content += "Recuperación de Nombre de Usuario</h1></header>"
            html_content += f"""
                <div class="content">
                    <p>Estimado usuario,</p>
                    <p>Este es su nombre de usuario registrado en el sistema: <span class="highlight">{username}</span>.</p>
                    <p>Si no ha solicitado este mensaje, por favor ignore este correo.</p>
                </div>"""
        case _:
            html_content = None
        
    if not html_content:
        return "Error: El tipo de correo no es válido."

    html_content += f"""
            <footer class="footer">
                © {año_actual} {NOMBRE_ASISTENTE}. Todos los derechos reservados.
            </footer>
        </div>
    </body>
    </html>
    """
    return html_content


def send_email(email, username=None, email_type=None):
    try:
        code = None

        # Generar el código de verificación si es necesario
        if email_type == 'password_recovery':
            code = create_code()
            headers = {
                "Content-Type": "application/json"
            }

            payload = {
                "code": f"{code}",
                "user_id": f"{st.session_state['user_id']}"
            }
            print(f"[send_email] Se envía estos valores a la api {payload}")
            response = requests.post(f"{BACKEND_URL}/create-code", json=payload, headers=headers)
            # Verificamos la respuesta de la API al crear el código
            if response.status_code == 200:
                response_json = response.json()  # Obtenemos el objeto completo de la respuesta
                # Imprimimos la respuesta de la API (opcional)
                print(f"[send_email] Response from API: {response_json}")
            else:
                print(f"Respuesta completa de response: {response}")
                print(f"[send_email] Error al crear el código, status code: {response.status_code}")
                return json.dumps({"success": False, "message": "Error al crear el código"})

        # Obtener el contenido HTML del correo
        html_content = generate_email_content(email_type, username, code)
        if html_content == "Error: El tipo de correo no es válido.":
            print(f"[send_email] html_content: {html_content}")
            return json.dumps({"success": False})

        # Obtener el asunto del correo
        subject = get_subject(email_type)
        if subject == "Error: El tipo de correo no es válido.":
            print(f"[send_email] subject: {subject}")
            return json.dumps({"success": False})

        # Configuración del destinatario y envío del correo
        sender = {"name": f"{NOMBRE_ASISTENTE}", "email": f"{EMAIL_SENDER}"}
        to = [{"email": f"{email}", "name": f"{username}"}]

        # Configuración y envío de email
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=html_content, sender=sender, subject=subject)
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(f"[send_email] email: {email}")
        print(f"[send_email] username: {username}")
        print(f"[send_email] email_type: {email_type}")
        print(f"[send_email] code: {code}")
        print(f"[send_email] html_content: {html_content}")
        print(f"[send_email] subject: {subject}")
        print(f"[send_email] sender: {sender}")
        print(f"[send_email] to: {to}")
        print(f"Correo enviado a: {email}")
        # Al final de todo el proceso, devolvemos el objeto con el código y los detalles
        return json.dumps({
            "success": True,
            "data": response_json if 'response_json' in locals() else None
        })

    except ApiException as e:
        print(f"Error al enviar el correo: {e}")
        return json.dumps({"success": False, "code": None})
