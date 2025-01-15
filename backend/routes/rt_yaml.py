from fastapi import APIRouter
from models.database import SessionLocal
from models.user import User
import yaml
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/generate-yaml")
async def generate_yaml():
    # Estructura base del archivo YAML
    data = {
        'cookie': {
            'expiry_days': 30,
            'key': 'some_signature_key',
            'name': 'some_cookie_name'
        },
        'credentials': {
            'usernames': {}
        },
        'oauth2': {
            'google': {
                'client_id': '',
                'client_secret': '',
                'redirect_uri': ''
            },
            'microsoft': {
                'client_id': '',
                'client_secret': '',
                'redirect_uri': '',
                'tenant_id': ''
            }
        },
        'pre-authorized': {
            'emails': ['melsby@gmail.com']
        }
    }

    # Obtener la sesión de la base de datos
    db = SessionLocal()

    # Obtener todos los usuarios
    usuarios = db.query(User).all()

    # Añadir usuarios a la estructura YAML
    for usuario in usuarios:
        data['credentials']['usernames'][usuario.email] = {
            'email': usuario.email,
            'failed_login_attempts': usuario.failed_login_attempts,
            'first_name': usuario.first_name,
            'last_name': usuario.last_name,
            'logged_in': usuario.logged_in,
            'password': usuario.password,  # Recuerda cifrar la contraseña
            'roles': usuario.roles if usuario.roles else []  # Roles opcionales
        }

    # Escribir el archivo YAML
    yaml_file_path = "config.yaml"
    with open(yaml_file_path, 'w') as archivo_yaml:
        yaml.dump(data, archivo_yaml, default_flow_style=False)

    # Retornar el archivo YAML generado como respuesta
    return FileResponse(yaml_file_path, media_type='application/x-yaml', filename="config.yaml")
