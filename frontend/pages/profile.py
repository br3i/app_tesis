import streamlit as st
import streamlit_authenticator as stauth
from modules.admin.utils.config_utils import load_config, save_config
from streamlit_authenticator.utilities import (RegisterError, ResetError, UpdateError)

#!!!!!!!!!!!!!!!!!CORREGIR EL MANEJO DE SESSION!!!!!!!!!!!!!!!!!!!!!!!
# VERIFICAR LOGIN

st.header('Página :green[Perfil]', divider="orange")

config = load_config()

# Verificar si el usuario está logueado
if "config_loaded" not in st.session_state:
    st.session_state["config_loaded"] = config

authenticator = stauth.Authenticate(
    st.session_state["config_loaded"]['credentials'],
    st.session_state["config_loaded"]['cookie']['name'],
    st.session_state["config_loaded"]['cookie']['key'],
    st.session_state["config_loaded"]['cookie']['expiry_days']
)


# Creating a password reset widget

try:
    if authenticator.reset_password(st.session_state["username"]):
        st.success('Password modified successfully')
        save_config(config)
except ResetError as e:
    st.error(e)
except CredentialsError as e:
    st.error(e)
    save_config(config)
st.write('_If you use the password reset widget please revert the password to what it was before once you are done._')
st.write('___')
try:
    if authenticator.update_user_details(st.session_state["username"]):
        st.success('Entries updated successfully')
except UpdateError as e:
    st.error(e)
st.write('___')
st.write('___')