import hashlib


def hash_password(password, salt=""):
    """Password hashing"""
    password_bytes = password.encode("utf-8") + salt.encode("utf-8")
    hash_object = hashlib.sha256(password_bytes)
    return hash_object.hexdigest()
