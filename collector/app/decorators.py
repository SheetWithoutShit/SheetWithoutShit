"""This module helpers decorators for collector app."""

import os

from aiohttp import web

from core.jwt import decode_jwt


def permission_required(func):
    """Check if client has correct permission to save transaction data."""
    secret_key = os.environ["SECRET_KEY"]

    def wrapper(request, *args, **kwargs):
        nonlocal secret_key
        token = request.match_info["token"]
        decoded_token = decode_jwt(token, secret_key)
        if not decoded_token:
            return web.json_response(
                data={"message": "Forbidden. Please provide correct user token."},
                status=403
            )

        request.user_id = decoded_token.get("user_id")
        return func(request, *args, **kwargs)

    return wrapper
