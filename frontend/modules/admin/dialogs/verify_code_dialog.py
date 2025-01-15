import streamlit as st
import json
import requests

BACKEND_URL = st.secrets.get("BACKEND_URL", "Not found")

@st.dialog("Ingrese el código enviado a su correo electrónico.", width="small")
def verify_code_dialog():
    print("[verify_code_dialog] st.session_state(verification_code): ", st.session_state["verification_code"])
    try:
        with st.form("verification_form"):
            # Campo para ingresar el código
            code = st.text_input("Código de verificación:", max_chars=6)

            # Botón para enviar el código
            submit_button = st.form_submit_button("Verificar")

            if submit_button:
                if code == st.session_state["verification_code"]["code"]:
                    response_vfy = requests.post(f"{BACKEND_URL}/verify-code", json={"code": code})
                    result = response_vfy.json()
                    if result['success']:
                        st.success("¡Código verificado con éxito! Espere un momento", icon=':material/check:')
                        st.session_state['code_right'] = True
                        st.session_state["code_sent"] = None
                        try:
                            response_up_status = requests.put(
                                f"{BACKEND_URL}/update-code-status/{st.session_state['verification_code']['id']}",
                                json={
                                    "status": 'used'
                                }
                            )
                            print(response_up_status.json())
                        except requests.exceptions.RequestException as e:
                            print(f"Error en la solicitud: {e}")
                        st.rerun()
                    else:
                        st.error(result['message'], icon=':material/gpp_maybe:')
                else:
                    st.error("El código ingresado no es válido. Por favor, intente nuevamente.", icon=':material/gpp_maybe:')
            else:
                st.info("Por favor, ingrese el código enviado al correo asociado.", icon=":material/info:")
    except Exception as e:
        st.error(f"Ocurrió un error: {e}", icon=':material/gpp_maybe:')