import base64
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

salt = os.urandom(16)
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=390000,
)


def get_func(password: str):
    key = base64.urlsafe_b64encode(kdf.derive(bytes(password)))
    return Fernet(key)


def encrypt(password: str, data: str) -> bytes:
    """Encrypt the JSON string."""
    crypt_func = get_func(password)
    return crypt_func.encrypt(bytes(data))


def decrypt(password: str, data: bytes) -> bytes:
    crypt_func = get_func(password)
    return crypt_func.decrypt(data)
