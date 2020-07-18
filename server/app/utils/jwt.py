"""This module provides functionality to work with JWT."""

import jwt


def decode_jwt(token, secret_key):
    """Try to decode JWT with secret key."""
    try:
        token = jwt.decode(token, secret_key)
    except (jwt.ExpiredSignatureError, jwt.DecodeError):
        pass

    return token
