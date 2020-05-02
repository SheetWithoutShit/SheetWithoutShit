"""This module provides middlewares for server app."""

import os
from aiohttp import web


@web.middleware
async def check_auth(request, handler):
    """Check if `Authorization` headers is correct."""
    auth_token = request.headers.get("Authorization")
    bot_token = os.environ["TELEGRAM_BOT_TOKEN"]

    if auth_token != bot_token:
        return web.json_response(
            data={"message": "You aren't authorized. Please provide correct authorization token."},
            status=401
        )

    return await handler(request)
