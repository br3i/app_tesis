import requests
import json
import streamlit as st
from helpers.send_email import send_email
from helpers.show_email import show_email

BACKEND_URL = st.secrets.get("BACKEND_URL", "Not found")

@st.dialog("Olvidó la contraseña?", width="small")
def forgot_password_dialog():
    try:
        with st.form("forgot_password_form"):
            st.subheader('Ingrese su nombre de usuario')
            username_fp = st.text_input('Usuario', placeholder="Ingrese su nombre de usuario")
            btn_forg_passw = st.form_submit_button('Buscar', type='primary')
            
            if btn_forg_passw and username_fp:
                response_fp = requests.get(f"{BACKEND_URL}/user/username/{username_fp}")
                if response_fp.status_code == 200:
                    st.session_state["username"] = username_fp
                    st.session_state['user_id'] = response_fp.json()["id"]
                    st.session_state['user_email'] = response_fp.json()["email"]
                    print(f"[forgor_pass_dialog user_id]: {st.session_state['user_id']}")

                    response_send_email = send_email(st.session_state["user_email"], username_fp, email_type='password_recovery')
                    result = json.loads(response_send_email)
                    with st.spinner('Procesando...'):
                        if result['success']:
                            st.success(f"El código de verificación ha sido enviado a {show_email(st.session_state['user_email'])}")
                            st.session_state["username_sent"] = True
                            st.session_state["code_sent"] = True
                            st.session_state["verification_code"] = result["data"]
                            st.rerun()
                        else:
                            st.error("Error al enviar el correo de recuperación.", icon=":material/gpp_maybe:")
                elif response_fp.status_code == 404:
                    st.error(response_fp.json()['detail'], icon=":material/gpp_maybe:")
            elif not username_fp:
                st.info("Ingrese el nombre de usuario para buscarlo", icon=":material/info:")
    except Exception as e:
        st.error(e, icon=":material/gpp_maybe:")