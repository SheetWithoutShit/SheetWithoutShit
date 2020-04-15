"""This module provides app initialization."""

import sys

from aiohttp.web import Application, run_app

from monobank.api import MonoBankAPI
from utils.settings import get_config
from views import routes


async def init_app(app):
    """Initialize application with routes."""
    app.add_routes(routes)
    app['monobank_api'] = MonoBankAPI()
    yield
    # todo: close HTTP session here


def main(argv):
    """Create app instance and run it."""
    app = Application()
    init_app(app)
    app.cleanup_ctx.append(init_app)
    config = get_config(argv)
    run_app(app,
            host=config['host'],
            port=config['port'])


if __name__ == '__main__':
    main(sys.argv[1:])
