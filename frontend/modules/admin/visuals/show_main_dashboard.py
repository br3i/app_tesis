import streamlit as st
from datetime import datetime
from modules.admin.utils.active_users import active_users
from modules.admin.utils.get_requested_document import get_len_requested_document
from modules.admin.utils.notifications_created import notifications_created
from modules.documents.decorators.get_documents_from_db import get_len_documents_from_db

MAX_NOTIFICATIONS_HEIGHT = st.secrets.get("MAX_NOTIFICATIONS_HEIGHT", 10)


def show_main_dashboard():
    st.header(
        "Dashboard de :orange[Administración] :material/admin_panel_settings:",
        divider="orange",
    )

    # Mostrar el contenido que no depende de las métricas
    st.subheader("Accesos Rápidos")
    cols = st.columns([0.25, 0.25, 0.25, 0.25], gap="small", vertical_alignment="top")

    with cols[0]:
        if st.button(
            ":material/account_box: Perfil", key="btn_profile", use_container_width=True
        ):
            st.switch_page("pages/profile.py")

    with cols[1]:
        if st.button(
            ":material/group: Usuarios", key="btn_users", use_container_width=True
        ):
            st.switch_page("pages/users.py")

    with cols[2]:
        if st.button(
            ":material/folder: Documentos",
            key="btn_documents",
            use_container_width=True,
        ):
            st.switch_page("pages/documents.py")

    with cols[3]:
        if st.button(
            ":material/bar_chart: Reportes", key="btn_reports", use_container_width=True
        ):
            st.switch_page("pages/reports.py")

    st.write("___")

    # Notificaciones
    st.subheader("Notificaciones Recientes")

    notifications = notifications_created()

    #!!!!!!!!!!!!!!!!!!!!!!!!!AGREGAR CONTROL DE ROLES!!!!!!!!!!!!!!!!!!!!!!!!!
    # Verificar los roles del usuario
    user_roles = st.session_state.get("roles", ["admin"])

    # Mostrar las notificaciones si el usuario tiene roles
    if notifications:
        len_notifications = len(notifications)

        # Limitar la altura máxima
        max_height = MAX_NOTIFICATIONS_HEIGHT * 35  # Altura máxima en píxeles
        container_height = min(len_notifications * 180, max_height)
        with st.container(height=container_height, border=False):
            for notification in notifications:
                with st.container(border=True):
                    with st.spinner("Cargando Notificación"):
                        # time.sleep(2)
                        # Verificar si el usuario tiene algún rol que coincide con los roles de la notificación
                        if any(role in user_roles for role in notification["roles"]):
                            kind = notification["kind"]
                            title = notification["title"]
                            message = notification["message"]
                            created_at = datetime.strptime(
                                notification["created_at"], "%Y-%m-%dT%H:%M:%S.%f"
                            )

                            # Extraer solo la hora del objeto datetime
                            formatted_datetime = created_at.strftime("%Y-%m-%d")

                            # Mostrar la notificación según el tipo de "kind"
                            if kind == "urgent":
                                st.markdown(
                                    f"_Creada el :red-background[{formatted_datetime}]_"
                                )
                                st.error(f"⚠️ **{title}**: {message}")
                            elif kind == "normal":
                                st.markdown(
                                    f"_Creada el :green-background[{formatted_datetime}]_"
                                )
                                st.success(f"ℹ️ **{title}**: {message}")
                            elif kind == "reminder":
                                st.markdown(
                                    f"_Creada el :orange-background[{formatted_datetime}]_"
                                )
                                st.warning(f"🔔 **{title}**: {message}")
                            elif kind == "informative":
                                st.markdown(
                                    f"_Creada el :blue-background[{formatted_datetime}]_"
                                )
                                st.info(f"📢 **{title}**: {message}")
                            elif kind == "alert":
                                st.markdown(
                                    f"_Creada el :red-background[{formatted_datetime}]_"
                                )
                                st.error(f"🚨 **{title}**: {message}")
                            else:
                                st.markdown(
                                    f"_Creada el :gray-background[{formatted_datetime}]_"
                                )
                                st.write(f"**{title}**: {message}")
    else:
        st.info("No hay notificaciones disponibles")

    # Ahora, comenzar a mostrar las métricas
    st.subheader("Resumen del Sistema")

    # Usamos st.empty para crear lugares vacíos en cada columna
    # Primera fila (2 columnas)
    col4, col5 = st.columns(2)

    with col4:
        placeholder_users = st.empty()  # Creamos un espacio vacío para los usuarios

    with col5:
        placeholder_docs_consulted = (
            st.empty()
        )  # Otro espacio vacío para los documentos

    # Segunda fila (2 columnas)
    col6, col7 = st.columns(2)

    with col6:
        placeholder_docs_loaded = st.empty()  # Otro espacio vacío para los documentos

    with col7:
        placeholder_reports = st.empty()  # Otro espacio vacío para los reportes

    # Usamos un spinner para simular la carga
    with st.spinner("Cargando métricas de Usuarios..."):
        n_users = active_users()  # Aquí usas la función real para obtener los usuarios
        placeholder_users.metric(
            "Usuarios Registrados",
            n_users,
            help="Usuarios registrados en la Base de Datos",
            label_visibility="visible",
            border=True,
        )

    with st.spinner("Cargando métricas de Documentos Consultados..."):
        n_documents_consulted = get_len_requested_document()
        placeholder_docs_consulted.metric(
            "Documentos Consultados",
            n_documents_consulted,
            help="Documentos consultados",
            label_visibility="visible",
            border=True,
        )

    with st.spinner("Cargando métricas de Documentos Cargados..."):
        n_documents_loaded = get_len_documents_from_db()
        placeholder_docs_loaded.metric(
            "Documentos Cargados",
            n_documents_loaded,
            help="Documentos cargados en la Base de Datos",
            label_visibility="visible",
            border=True,
        )

    with st.spinner("Cargando métricas de Reportes Generados..."):
        n_reports = 0  # Aquí puedes sustituir con la función real para obtener reportes generados
        placeholder_reports.metric(
            "Reportes Generados",
            n_reports,
            help="Reportes Generados",
            label_visibility="visible",
            border=True,
        )
