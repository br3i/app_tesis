import streamlit as st
import os
import toml

@st.cache_data(show_spinner=False, ttl=60)
def load_theme_config():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "../../../.streamlit/config.toml")

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"El archivo config.toml no se encontró en: {config_path}")

    config = toml.load(config_path)
    
    theme_config = config.get('theme', {})

    # Retornar los valores de configuración si es necesario
    return theme_config
