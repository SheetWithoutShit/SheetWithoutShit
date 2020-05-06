"""This module provides middlewares for server app."""

from aiohttp import web


@web.middleware
async def check_auth(request, handler):
    """Check if `Authorization` headers is correct provided."""
    telegram_token = request.app["constants"]["TELEGRAM_TOKEN"]
    auth_token = request.headers.get("Authorization")

    if auth_token != telegram_token:
        return web.json_response(
            data={"message": "You aren't authorized. Please provide correct authorization token."},
            status=401
        )

    return await handler(request)
