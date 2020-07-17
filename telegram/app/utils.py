"""This module provides helper functionality."""

import datetime

import jwt


DEFAULT_EXP_TIME = 86400


def encode_jwt(data, secret_key, exp_time=DEFAULT_EXP_TIME):
    """Create JWT for data payload with secret key and certain expiration time."""
    data["exp"] = datetime.datetime.now() + datetime.timedelta(seconds=exp_time)
    token = jwt.encode(data, secret_key)

    return token
