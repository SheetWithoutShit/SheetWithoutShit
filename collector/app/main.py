"""This module provides app initialization."""

import os
import asyncio

from aiohttp.web import Application, run_app

from views import routes
from monobank.api import MonoBankAPI
from spreadsheet.api import SpreadsheetAPI
from spreadsheet.auth import SpreadsheetAuth
from core.database import PoolManager


async def init_clients(app):
    """Initialize application with clients."""
    app["monobank_api"] = monobank_api = MonoBankAPI()
    app["spreadsheet_api"] = spreadsheet_api = SpreadsheetAPI()
    app["spreadsheet_auth"] = spreadsheet_auth = SpreadsheetAuth()
    app["postgres"] = postgres = await PoolManager.create()

    yield

    await asyncio.gather(
        monobank_api.close(),
        spreadsheet_api.close(),
        spreadsheet_auth.close(),
        postgres.close()
    )


# TODO: read about debug mode
def main():
    """Create aiohttp web server and run it."""
    app = Application()
    app.add_routes(routes)
    app.cleanup_ctx.append(init_clients)

    host = os.environ.get("DEFAULT_HOST", "127.0.0.1")
    port = os.environ.get("DEFAULT_PORT", 8000)
    run_app(
        app,
        host=host,
        port=port
    )


if __name__ == '__main__':
    main()
