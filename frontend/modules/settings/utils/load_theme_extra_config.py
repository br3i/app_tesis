import streamlit as st
import os
import toml

@st.cache_data(show_spinner=False, ttl=60)
def load_theme_extra_config():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "../../../.streamlit/extra_config.toml")

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"El archivo config.toml no se encontró en: {config_path}")

    config = toml.load(config_path)
    
    extra_theme_config = config.get('color_pages', {})    

    # Retornar los valores de configuración si es necesario
    return extra_theme_config
