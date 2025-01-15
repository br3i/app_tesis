import streamlit as st
import json
import requests
from helpers.send_email import send_email

BACKEND_URL = st.secrets.get("BACKEND_URL", "Not found")

@st.dialog("Olvidó el nombre de usuario?", width="small")
def forgot_username_dialog():
    try:
        with st.form("forgot_username_form"):
            st.subheader('Recuperar nombre de Usuario')
            email_fu = st.text_input('Email', placeholder="Ingrese su email")
            btn_forg_username = st.form_submit_button('Buscar', type='primary')

            if btn_forg_username:
                response_fu = requests.get(f"{BACKEND_URL}/user/email/{email_fu}")
                response_data = response_fu.json()

                if "detail" not in response_data:
                    response_send_email = send_email(email_fu, response_data['username'], email_type='username_recovery')
                    print(f"\n\nresponse-send-email {response_send_email}")
                    #Convertir dict a json
                    response_data = json.loads(response_send_email)
                    if response_data["success"]:
                        st.session_state["email_recovery_sent"] = True
                        st.success("El nombre de usuario ha sido enviado a su correo",  icon=":material/check:")
                    else:
                        st.error(f"Error al enviar el correo.", icon=":material/gpp_maybe:")
                elif not email_fu:
                    st.info("Ingrese un email para buscarlo", icon=":material/info:")
                elif not response_fu:
                    st.error(response_data['detail'], icon=":material/gpp_maybe:")
    except Exception as e:
        st.error(e, icon=":material/gpp_maybe:")