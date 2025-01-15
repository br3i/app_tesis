import streamlit as st
import uuid

def reset_df_dlt():
    st.session_state.df_key_dlt = str(uuid.uuid4())