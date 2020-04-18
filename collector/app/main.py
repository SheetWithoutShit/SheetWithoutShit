"""This module provides app initialization."""

import os
import asyncio
import logging

from aiohttp.web import Application, run_app

from views import routes
from core.monobank.api import MonoBankAPI
from core.spreadsheet.api import SpreadsheetAPI
from core.spreadsheet.auth import SpreadsheetAuth
from core.database.postgres import PoolManager as PGPoolManager
from core.database.redis import PoolManager as RedisPoolManager


def init_logger():
    """Initialize stream and file logger if it is available."""
    log_format = "%a %t [VIEW: %r] [RESPONSE: %s (%bb)] [TIME: %Dms]"

    logger = logging.getLogger("aiohttp.access")
    logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    logger.addHandler(stream_handler)

    log_dir = os.environ.get("COLLECTOR_LOG_DIR")
    log_filepath = f'{log_dir}/collector.log'
    if log_dir and os.path.exists(log_filepath) and os.access(log_filepath, os.W_OK):
        file_handler = logging.FileHandler(log_filepath)
        logger.addHandler(file_handler)

    return logger, log_format


async def init_clients(app):
    """Initialize application with clients."""
    app["monobank_api"] = monobank_api = MonoBankAPI()
    app["spreadsheet_api"] = spreadsheet_api = SpreadsheetAPI()
    app["spreadsheet_auth"] = spreadsheet_auth = SpreadsheetAuth()
    app["postgres"] = postgres = await PGPoolManager.create()
    app["redis"] = redis = await RedisPoolManager.create()

    yield

    await asyncio.gather(
        monobank_api.close(),
        spreadsheet_api.close(),
        spreadsheet_auth.close(),
        postgres.close(),
        redis.close()
    )


# TODO: read about debug mode
def main():
    """Create aiohttp web server and run it."""
    host = os.environ.get("COLLECTOR_HOST", "127.0.0.1")
    port = os.environ.get("COLLECTOR_PORT", 8000)

    logger, log_format = init_logger()
    app = Application(logger=logger)
    app.add_routes(routes)
    app.cleanup_ctx.append(init_clients)

    run_app(
        app,
        host=host,
        port=port,
        access_log_format=log_format
    )


if __name__ == '__main__':
    main()
