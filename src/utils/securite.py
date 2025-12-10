# pas utiliser pour le projet mais on le garde si on veux hasher les mots de passe

import hashlib


def hash_password(password, sel=""):
    """Hachage du mot de passe"""
    password_bytes = password.encode("utf-8") + sel.encode("utf-8")
    hash_object = hashlib.sha256(password_bytes)
    return hash_object.hexdigest()
