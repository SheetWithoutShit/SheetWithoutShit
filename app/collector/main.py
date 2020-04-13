"""This module provides app initialization."""

from aiohttp.web import Application, run_app

from collector.views import routes


async def init_app():
    """Initialize application with routes"""
    app = Application()
    app.add_routes(routes)
    return app


# todo: move this to app package into manager
def main():
    """Run app on certain host and port"""
    app = init_app()
    run_app(app, port=8000)
