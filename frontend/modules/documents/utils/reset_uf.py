import streamlit as st
import uuid

def reset_uf():
    st.session_state.uf_key = str(uuid.uuid4())