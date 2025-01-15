import secrets
import string

def create_code(length=6) -> str:
    return ''.join(secrets.choice(string.digits) for _ in range(length))
