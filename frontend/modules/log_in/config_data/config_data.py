import streamlit as st
import os
import yaml
import pytz
from datetime import datetime
from pathlib import Path
from datetime import datetime, timedelta
from modules.log_in.cache_data.load_data import load_users

current_dir = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.abspath(
    os.path.join(current_dir, "..", "..", "..", "config", "config.yaml")
)
print("Config_file: ", CONFIG_FILE)
TIME_ZONE = st.secrets.get("TIME_ZONE", "Not Found")

tz = pytz.timezone(TIME_ZONE)

# Datos predeterminados para el primer inicio
default_config = {
    "cookie": {
        "expiry_days": 1,
        "key": "key_sistere",
        "name": "cookie_sistere",
        "last_date": None,  # Inicialmente no hay fecha
    },
    "credentials": {"usernames": {}},
}


# Verificar si el archivo de configuración existe y crear si no
def initialize_config():
    if not os.path.exists(CONFIG_FILE):
        print(
            f"Archivo de configuración no encontrado. Creando uno nuevo en {CONFIG_FILE}"
        )
        with open(CONFIG_FILE, "w") as file:
            yaml.dump(default_config, file)
        update_users_in_yaml()


def load_config():
    initialize_config()  # Asegúrate de inicializar el archivo si no existe
    with open(CONFIG_FILE, "r") as file:
        return yaml.safe_load(file)


def save_config(data):
    """Guarda la configuración en el archivo YAML."""
    print("[save_config]")
    with open(CONFIG_FILE, "w") as file:
        yaml.dump(data, file)


def is_session_valid(username):
    """Verifica si la sesión del usuario sigue activa."""
    config = load_config()
    user_data = config["credentials"]["usernames"].get(username)
    if not user_data or not user_data.get("logged_in"):
        return False
    last_login = datetime.fromisoformat(user_data["last_login"])
    expiry_days = config["cookie"]["expiry_days"]
    current_time = datetime.now(tz)
    return current_time - last_login <= timedelta(days=expiry_days)


def update_users_in_yaml():
    """Cargar los usuarios desde la base de datos y agregar o actualizar en el archivo YAML usando el id como clave única."""
    load_users.clear()
    users = load_users()
    print("[update_users_in_yaml] users: ", users)
    if users:
        config = load_config()
        id_mapping = {
            v.get("id"): k for k, v in config["credentials"]["usernames"].items()
        }

        for user in users:
            user_id = user["id"]
            if user_id in id_mapping:
                # Encontrar el username actual basado en el id
                current_username = id_mapping[user_id]
                # Actualizar los datos existentes
                config["credentials"]["usernames"][current_username] = {
                    "email": user["email"],
                    "first_name": user["first_name"],
                    "last_name": user["last_name"],
                    "logged_in": config["credentials"]["usernames"][
                        current_username
                    ].get("logged_in", False),
                    "last_login": config["credentials"]["usernames"][
                        current_username
                    ].get("last_login", None),
                    "roles": user["roles"],
                    "id": user_id,  # Asegurarnos de mantener el id
                }
                # Si cambió el username, renombrar la clave en el YAML
                if current_username != user["username"]:
                    config["credentials"]["usernames"][user["username"]] = config[
                        "credentials"
                    ]["usernames"].pop(current_username)
            else:
                # Si no existe el usuario, crearlo
                config["credentials"]["usernames"][user["username"]] = {
                    "email": user["email"],
                    "first_name": user["first_name"],
                    "last_name": user["last_name"],
                    "logged_in": False,
                    "last_login": None,
                    "roles": user["roles"],
                    "id": user_id,
                }

        save_config(config)


def sync_deleted_users():
    """
    Sincroniza y elimina usuarios del archivo de configuración YAML que ya no están en la base de datos.
    """
    # Cargar usuarios actuales desde la base de datos
    load_users.clear()
    users_from_db = load_users()

    # Cargar configuración desde el archivo YAML
    config = load_config()

    # Obtener IDs de usuarios desde la base de datos
    db_user_ids = {user["id"] for user in users_from_db} if users_from_db else set()

    # Crear un mapeo entre usernames e IDs en el archivo YAML
    yaml_user_ids = {
        username: details["id"]
        for username, details in config["credentials"]["usernames"].items()
        if "id" in details
    }

    # Identificar usuarios que ya no están en la base de datos
    users_to_remove = [
        username
        for username, user_id in yaml_user_ids.items()
        if user_id not in db_user_ids
    ]

    # Eliminar usuarios obsoletos del archivo YAML
    for username in users_to_remove:
        del config["credentials"]["usernames"][username]
        print(f"Usuario eliminado del archivo de configuración: {username}")

    # Guardar los cambios en el archivo YAML
    save_config(config)
    print(f"{len(users_to_remove)} usuarios eliminados del archivo de configuración.")


def logout_user(username):
    """Cierra la sesión del usuario especificado."""
    config = load_config()  # Cargar la configuración actual
    user_data = config["credentials"]["usernames"].get(username)

    if user_data:
        # Actualizar el campo logged_in a false
        user_data["logged_in"] = False
        # Opcional: Actualizar la fecha de cierre de sesión, si deseas llevar un registro
        user_data["last_login"] = (
            None  # O usa datetime.now(tz).isoformat() si quieres registrar algo
        )
        # Guardar los cambios en el archivo de configuración
        save_config(config)
        print(f"Usuario '{username}' cerrado correctamente.")
    else:
        print(f"Usuario '{username}' no encontrado en el archivo de configuración.")


# Función para manejar el cierre de sesión
def handle_logout():
    username = st.session_state.get("username")
    if username:
        print("[config_data] username :", username)
        logout_user(username)
        st.session_state.clear()
        st.rerun()
