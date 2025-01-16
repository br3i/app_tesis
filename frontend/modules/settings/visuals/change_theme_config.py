import streamlit as st
from modules.settings.utils.save_theme_changes import save_theme_changes

NOMBRE_ASISTENTE = st.secrets.get('NOMBRE_ASISTENTE', 'Not found')

def change_theme_config(theme_config, theme_extra_config):
    # Acceder a valores
    primaryColor = theme_config["primaryColor"]
    backgroundColor = theme_config["backgroundColor"]
    secondaryBackgroundColor = theme_config["secondaryBackgroundColor"]
    textColor = theme_config["textColor"]
    font = theme_config["font"]

    color_options = ["blue", "green", "orange", "red", "violet", "gray", "rainbow"]
    font_options = ["sans serif", "serif", "monospace"]

    font_index = font_options.index(font) if font in font_options else 0

    primary_config_color = theme_extra_config["primary_config_color"]
    secondary_config_color = theme_extra_config["secondary_config_color"]
    primary_config_index = color_options.index(primary_config_color) if primary_config_color in color_options else 0
    secondary_config_index = color_options.index(secondary_config_color) if secondary_config_color in color_options else 0

    primary_docs_color = theme_extra_config["primary_docs_color"]
    secondary_docs_color = theme_extra_config["secondary_docs_color"]
    primary_docs_index = color_options.index(primary_docs_color) if primary_docs_color in color_options else 0
    secondary_docs_index = color_options.index(secondary_docs_color) if secondary_docs_color in color_options else 0

    primary_users_color = theme_extra_config["primary_users_color"]
    secondary_users_color = theme_extra_config["secondary_users_color"]
    primary_users_index = color_options.index(primary_users_color) if primary_users_color in color_options else 0
    secondary_users_index = color_options.index(secondary_users_color) if secondary_users_color in color_options else 0

    primary_reports_color = theme_extra_config["primary_reports_color"]
    secondary_reports_color = theme_extra_config["secondary_reports_color"]
    primary_reports_index = color_options.index(primary_reports_color) if primary_reports_color in color_options else 0
    secondary_reports_index = color_options.index(secondary_reports_color) if secondary_reports_color in color_options else 0

    primary_audit_color = theme_extra_config["primary_audit_color"]
    secondary_audit_color = theme_extra_config["secondary_audit_color"]
    primary_audit_index = color_options.index(primary_audit_color) if primary_audit_color in color_options else 0
    secondary_audit_index = color_options.index(secondary_audit_color) if secondary_audit_color in color_options else 0

    primary_documentation_color = theme_extra_config["primary_documentation_color"]
    secondary_documentation_color = theme_extra_config["secondary_documentation_color"]
    primary_documentation_index = color_options.index(primary_documentation_color) if primary_documentation_color in color_options else 0
    secondary_documentation_index = color_options.index(secondary_documentation_color) if secondary_documentation_color in color_options else 0

    primary_assistant_color = theme_extra_config["primary_assistant_color"]
    secondary_assistant_color = theme_extra_config["secondary_assistant_color"]
    primary_assistant_index = color_options.index(primary_assistant_color) if primary_assistant_color in color_options else 0
    secondary_assistant_index = color_options.index(secondary_assistant_color) if secondary_assistant_color in color_options else 0


    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        background = st.color_picker("Fondo", value=backgroundColor, key="background_color", help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")
        second_background = st.color_picker("Fondo secundario", value=secondaryBackgroundColor, key="sec_background_color", help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")

    with col2:
        primary = st.color_picker("Color primario", value=primaryColor, key="primary_color", help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")
        text_color= st.color_picker("Texto", value=textColor, key="text_color", help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")
    with col3:
        font = "sans serif"
        primaryColor = "#FF4B4B"
        if st.session_state.switch_theme == "light":
            backgroundColor = "#FFFFFF"
            secondaryBackgroundColor= "#F0F2F6"
            textColor = "#31333F"
        else:
            backgroundColor = "#0E1117"
            secondaryBackgroundColor= "#262730"
            textColor = "#FAFAFA"

        if st.button(
                "", 
                key="btn_change_default_values", 
                on_click=save_theme_changes, 
                kwargs={
                        "primaryColor": primaryColor, 
                        "backgroundColor": backgroundColor, 
                        "secondaryBackgroundColor": secondaryBackgroundColor, 
                        "textColor": textColor, 
                        "font": font,
                        "fast_change": True
                    }, 
                type="secondary", 
                icon=f":material/{st.session_state.switch_theme}_mode:"
            ):
            if st.session_state.switch_theme == "light":
                st.session_state.switch_theme = "dark"
            else:
                st.session_state.switch_theme = "light"
            st.rerun()


    with st.expander("Colores de páginas", icon=":material/select_window:"):
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("Archivos", divider=f"{primary_docs_color}")
            new_primary_docs_color = st.selectbox(
                "Color primario", color_options, 
                index=primary_docs_index, 
                key="new_primary_docs_color", 
                help=None,
                placeholder="Choose an option", 
                label_visibility="visible"
            )
            new_secondary_docs_color = st.selectbox(
                "Color secundario", 
                color_options, 
                index=secondary_docs_index, 
                key="new_secondary_docs_color", 
                help=None, 
                placeholder="Choose an option", 
                label_visibility="visible"
            )

            st.subheader("Reportes", divider=f"{primary_reports_color}")
            new_primary_reports_color = st.selectbox(
                "Color primario",
                color_options,
                index=primary_reports_index,  # Asigna el índice basado en el color seleccionado
                key="new_primary_reports_color",
                help=None,
                placeholder="Choose an option",
                label_visibility="visible"
            )
            new_secondary_reports_color = st.selectbox(
                "Color secundario",
                color_options,
                index=secondary_reports_index,  # Asigna el índice basado en el color seleccionado
                key="new_secondary_reports_color",
                help=None,
                placeholder="Choose an option",
                label_visibility="visible"
            )

            st.subheader("Documentación", divider=f"{primary_documentation_color}")
            new_primary_documentation_color = st.selectbox(
                "Color primario",
                color_options,
                index=primary_documentation_index,  # Asigna el índice basado en el color seleccionado
                key="new_primary_documentation_color",
                help=None,
                placeholder="Choose an option",
                label_visibility="visible"
            )
            new_secondary_documentation_color = st.selectbox(
                "Color secundario",
                color_options,
                index=secondary_documentation_index,  # Asigna el índice basado en el color seleccionado
                key="new_secondary_documentation_color",
                help=None,
                placeholder="Choose an option",
                label_visibility="visible"
            )

            st.subheader("Configuración", divider=f"{primary_config_color}")
            new_primary_config_color = st.selectbox(
                "Color primario",
                color_options,
                index=primary_config_index,
                key="new_primary_config_color",
                help="Selecciona el color primario para la configuración",
                placeholder="Elige una opción",
                label_visibility="visible"
            )

            new_secondary_config_color = st.selectbox(
                "Color secundario",
                color_options,
                index=secondary_config_index,
                key="new_secondary_config_color",
                help="Selecciona el color secundario para la configuración",
                placeholder="Elige una opción",
                label_visibility="visible"
            )
        with col2:
            st.subheader("Usuarios", divider=f"{primary_users_color}")
            new_primary_users_color = st.selectbox(
                "Color primario", color_options, 
                index=primary_users_index, 
                key="new_primary_users_color", 
                help=None, 
                placeholder="Choose an option", 
                label_visibility="visible"
            )
            new_secondary_users_color = st.selectbox(
                "Color secundario", color_options, 
                index=secondary_users_index, 
                key="new_secondary_users_color", 
                help=None,
                placeholder="Choose an option",
                label_visibility="visible"
            )

            st.subheader("Auditoria", divider=f"{primary_audit_color}")
            new_primary_audit_color = st.selectbox(
                "Color primario",
                color_options,
                index=primary_audit_index,  # Asigna el índice basado en el color seleccionado
                key="new_primary_audit_color",
                help=None,
                placeholder="Choose an option",
                label_visibility="visible"
            )

            new_secondary_audit_color = st.selectbox(
                "Color secundario",
                color_options,
                index=secondary_audit_index,  # Asigna el índice basado en el color seleccionado
                key="new_secondary_audit_color",
                help=None,
                placeholder="Choose an option",
                label_visibility="visible"
            )

            st.subheader(f"{NOMBRE_ASISTENTE}", divider=f"{primary_assistant_color}")
            new_primary_assistant_color = st.selectbox(
                "Color primario",
                color_options,
                index=primary_assistant_index,  # Asigna el índice basado en el color seleccionado
                key="new_primary_assistant_color",
                help=None,
                placeholder="Choose an option",
                label_visibility="visible"
            )

            new_secondary_assistant_color = st.selectbox(
                "Color secundario",
                color_options,
                index=secondary_assistant_index,  # Asigna el índice basado en el color seleccionado
                key="new_secondary_assistant_color",
                help=None,
                placeholder="Choose an option",
                label_visibility="visible"
            )

    text_font = st.selectbox(
            "Fuente", 
            font_options, 
            index=font_index, 
            help=None, 
            placeholder="Choose an option",
            label_visibility="visible"
        )
    
    kwargs_save_theme_changes = {
        "primaryColor": primary,
        "backgroundColor": background,
        "secondaryBackgroundColor": second_background,
        "textColor": text_color,
        "font": text_font,
        "new_primary_docs_color": new_primary_docs_color,
        "new_secondary_docs_color": new_secondary_docs_color,
        "new_primary_reports_color": new_primary_reports_color,
        "new_secondary_reports_color": new_secondary_reports_color,
        "new_primary_documentation_color": new_primary_documentation_color,
        "new_secondary_documentation_color": new_secondary_documentation_color,
        "new_primary_config_color": new_primary_config_color,
        "new_secondary_config_color": new_secondary_config_color,
        "new_primary_users_color": new_primary_users_color,
        "new_secondary_users_color": new_secondary_users_color,
        "new_primary_audit_color": new_primary_audit_color,
        "new_secondary_audit_color": new_secondary_audit_color,
        "new_primary_assistant_color": new_primary_assistant_color,
        "new_secondary_assistant_color": new_secondary_assistant_color,
        "fast_change": False
    }

    if st.button(
            "Guardar cambios", 
            key="btn_save_theme_changes", 
            on_click=save_theme_changes, 
            kwargs=kwargs_save_theme_changes, 
            type="secondary", 
            icon=":material/save:"
        ):
        st.rerun()