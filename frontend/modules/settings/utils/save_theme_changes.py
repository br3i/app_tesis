import streamlit as st
import os
import toml
from modules.settings.utils.load_theme_config import load_theme_config
from modules.settings.utils.load_theme_extra_config import load_theme_extra_config

def save_theme_changes(**kwargs):
    print("[save_theme_changes] kwargs: ", kwargs)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "../../../.streamlit/config.toml")
    config_extra_path = os.path.join(base_dir, "../../../.streamlit/extra_config.toml")
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"El archivo config.toml no se encontró en: {config_path}")
    
    if not os.path.exists(config_extra_path):
        raise FileNotFoundError(f"El archivo config_extra.toml no se encontró en: {config_extra_path}")

    # Cargar el contenido actual del archivo .toml
    config = toml.load(config_path)
    config_extra = toml.load(config_extra_path)

    # Acceder o crear la sección 'theme' si no existe
    theme_config = config.get('theme', {})
    theme_extra_config = config_extra.get('color_pages', {})

    # Actualizar los valores del tema con los valores proporcionados
    theme_config['primaryColor'] = kwargs['primaryColor']
    theme_config['backgroundColor'] = kwargs['backgroundColor']
    theme_config['secondaryBackgroundColor'] = kwargs['secondaryBackgroundColor']
    theme_config['textColor'] = kwargs['textColor']
    theme_config['font'] = kwargs['font']
    
    if kwargs['fast_change'] == False:
        theme_extra_config['primary_docs_color'] = kwargs['new_primary_docs_color']
        theme_extra_config['secondary_docs_color'] = kwargs['new_secondary_docs_color']
        theme_extra_config['primary_users_color'] = kwargs['new_primary_users_color']
        theme_extra_config['secondary_users_color'] = kwargs['new_secondary_users_color']
        theme_extra_config['primary_audit_color'] = kwargs['new_primary_audit_color']
        theme_extra_config['secondary_audit_color'] = kwargs['new_secondary_audit_color']
        theme_extra_config['primary_documentation_color'] = kwargs['new_primary_documentation_color']
        theme_extra_config['secondary_documentation_color'] = kwargs['new_secondary_documentation_color']
        theme_extra_config['primary_assistant_color'] = kwargs['new_primary_assistant_color']
        theme_extra_config['secondary_assistant_color'] = kwargs['new_secondary_assistant_color']
        theme_extra_config['primary_config_color'] = kwargs['new_primary_config_color']
        theme_extra_config['secondary_config_color'] = kwargs['new_secondary_config_color']

    # Asegurarse de que la sección 'theme' exista en el archivo de configuración
    config['theme'] = theme_config
    config_extra['color_pages'] = theme_extra_config

    # Guardar el archivo .toml con los nuevos valores
    with open(config_path, 'w') as config_file:
        toml.dump(config, config_file)
    
    with open(config_extra_path, 'w') as config_extra_file:
        toml.dump(config_extra, config_extra_file)
    
    load_theme_config.clear()
    load_theme_extra_config.clear()