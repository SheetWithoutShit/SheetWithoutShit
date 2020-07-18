"""This module provides middlewares for server app."""

from aiohttp import web

from core.jwt import decode_jwt


USER_PATH = "/user"


@web.middleware
async def check_auth(request, handler):
    """Check if client has correct token in case of accessing protected paths."""
    if request.path.startswith(USER_PATH):
        secret_key = request.app["constants"]["SECRET_KEY"]
        auth_token = request.headers.get("Authorization")
        decoded_token = decode_jwt(auth_token, secret_key)
        if not decoded_token:
            return web.json_response(
                data={"message": "You aren't authorized. Please provide correct authorization token."},
                status=401
            )
        request.user_id = decoded_token.get("user_id")

    return await handler(request)


@web.middleware
async def check_permission(request, handler):
    """Check if client has appropriate permissions."""
    if request.path.startswith(USER_PATH):
        telegram_id = int(request.match_info["telegram_id"])
        if telegram_id != request.user_id:
            return web.json_response(
                data={"message": "Forbidden. You don't have appropriate permission."},
                status=401
            )

    return await handler(request)
