"""This module provides app initialization."""

import os

from aiohttp.web import Application, run_app

from monobank.api import MonoBankAPI
from views import routes


async def init_app(app):
    """Initialize application with routes."""
    app.add_routes(routes)
    app['monobank_api'] = MonoBankAPI()
    yield
    # todo: close HTTP session here


def main():
    """Create app instance and run it."""
    app = Application()
    init_app(app)
    app.cleanup_ctx.append(init_app)
    host = os.getenv('DEFAULT_HOST', '127.0.0.1')
    port = int(os.getenv('DEFAULT_PORT', '8000'))
    run_app(
        app,
        host=host,
        port=port
    )


if __name__ == '__main__':
    main()
