import streamlit as st
import uuid

def reset_df_dlt_user():
    st.session_state.df_u_dlt_key= str(uuid.uuid4())
    