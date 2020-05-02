"""This module provides telegram bot client."""

import os

from telebot import TeleBot

from api import API


class Bot(TeleBot):
    """Class that provides telegram bot client."""

    def __init__(self):
        """Initialize telegram bot client."""
        token = os.environ["TELEGRAM_BOT_TOKEN"]
        server_host = os.environ["SERVER_HOST"]
        server_port = os.environ["SERVER_PORT"]
        domain = f"{server_host}:{server_port}"

        self.api = API(domain, token)
        super().__init__(token)
