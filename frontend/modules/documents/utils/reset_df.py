import streamlit as st
import uuid

def reset_df():
    st.session_state.df_key = str(uuid.uuid4())