import hashlib


def pass_hash(username, password):
    return hashlib.sha512((username + password).encode("utf-8")).hexdigest()