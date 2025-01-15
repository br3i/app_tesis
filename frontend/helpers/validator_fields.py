import streamlit as st
import re

MAX_PASSWORD_LENGTH = int(st.secrets.get('MAX_PASSWORD_LENGTH', 'Not found'))

def validate_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+-]{1,254}@[a-zA-Z0-9.-]{1,253}\.[a-zA-Z]{2,63}$"
    return bool(re.match(pattern, email))

def validate_length(variable: str, min_length: int=1, max_length: int=MAX_PASSWORD_LENGTH) -> bool:
    pattern = rf"^.{{{min_length},{max_length}}}$"
    return bool(re.match(pattern, variable))

def validate_name(name: str) -> bool:
    pattern = r"^[A-Za-z. ]{2,100}$"
    return bool(re.match(pattern, name))

def validate_password(password: str) -> bool:
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$"
    return bool(re.match(pattern, password))

def validate_username(username: str) -> bool:
    pattern = r"^([a-zA-Z0-9_-]{1,20}|[a-zA-Z0-9._%+-]{1,254}@[a-zA-Z0-9.-]{1,253}\.[a-zA-Z]{2,63})$"
    return bool(re.match(pattern, username))