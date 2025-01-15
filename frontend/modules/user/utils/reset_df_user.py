import streamlit as st
import uuid

def reset_df_user():
    st.session_state.users_df = st.session_state["original_roles_df"].copy()
    st.session_state.df_u_key= str(uuid.uuid4())
    