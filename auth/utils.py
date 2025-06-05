from passlib.context import CryptContext
import secrets

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> bytes:
    password_hash_str = pwd_context.hash(password)
    return password_hash_str.encode("utf-8")


def generate_token():
    return secrets.token_urlsafe(32)


def verify_password(plained_password, password):
    return pwd_context.verify(plained_password, password)
