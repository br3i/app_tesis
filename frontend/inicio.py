import streamlit as st

# Configurar el título y subtítulo para hacer la página más atractiva
st.title("¡Bienvenido a la Aplicación!")
st.subheader("Elige una opción para empezar")

# Añadir enlaces con botones estilizados
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔎 Ayuda", key="ayuda", use_container_width=True):
        st.switch_page("pages/help.py")

with col2:
    if st.button("🤖 Asistente", key="asistente", use_container_width=True):
        st.switch_page("pages/assistant.py")
    # Añadir imágenes decorativas si es necesario
    st.image("assets/hashcat.png")

with col3:
    if st.button("📁 Administración", key="admin", use_container_width=True):
        st.switch_page("pages/admin.py")


# O si quieres agregar algún mensaje adicional o información útil
st.text(
    "Si tienes alguna duda o necesitas ayuda, no dudes en consultar el asistente o el área de administración."
)
