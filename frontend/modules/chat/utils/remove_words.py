import streamlit as st

def remove_word(word):
    st.session_state.word_list.remove(word)