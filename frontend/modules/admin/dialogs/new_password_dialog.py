import streamlit as st
from modules.admin.utils.validate_password import validate_password
from modules.admin.utils.change_password import change_password


@st.dialog("Restablecer contraseña", width="small")
def new_password_dialog():
    # Captura en tiempo real del valor de la nueva contraseña
    new_password = st.text_input(
        "Nueva contraseña:",
        type="password",
        placeholder="Introduce tu nueva contraseña",
        label_visibility="visible",
        help=(
            """
            **Criterios:**
            - Debe tener entre 8 y 20 caracteres.
            - Debe contener al menos una letra mayúscula.
            - Debe contener al menos una letra minúscula.
            - Debe contener al menos un número.
            - Debe contener al menos un carácter especial de los siguientes [@$!%*?&].
            """
        ),
    )

    # Repetir la contraseña para confirmación
    new_password_2 = st.text_input(
        "Repetir contraseña:",
        key="password_repeat",
        type="password",
        placeholder="Repite tu nueva contraseña",
    )

    # Validar criterios de la contraseña
    if new_password:
        all_criteria_met, criteria = validate_password(new_password)

        # Mostrar los criterios de validación dinámicamente
        with st.expander("Criterios de la contraseña", expanded=True):
            for criterion, met in criteria.items():
                icon = "✅" if met else "❌"
                st.write(f"{icon} {criterion}")

        # Confirmar cambio de contraseña
        if st.button("Cambiar contraseña"):
            if not all_criteria_met:
                st.error(
                    "La contraseña no cumple con todos los criterios.",
                    icon=":material/gpp_maybe:",
                )
            elif new_password != new_password_2:
                st.error("Las contraseñas no coinciden.", icon=":material/gpp_maybe:")
            else:
                st.session_state["code_sent"] = None
                st.session_state["code_right"] = None
                user_id = st.session_state.get("user_id")
                if user_id is not None and change_password(user_id, new_password):
                    st.session_state["password_changed"] = True
                    st.success(
                        "¡Contraseña cambiada exitosamente!", icon=":material/check:"
                    )
                    st.rerun()
                else:
                    st.session_state["password_changed"] = False
