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

        self.api = API(domain)
        self.commands = []
        super().__init__(token)

    def add_message_handler(self, handler_dict):
        """Add name of message handler."""
        super().add_message_handler(handler_dict)

        commands_names = handler_dict["filters"]["commands"] or []
        commands = [f"/{command}" for command in commands_names]
        self.commands.extend(commands)

    def check_command(self, func):
        """Process command if it was provided by user."""
        def wrapper(message, *args, **kwargs):
            if any([message.text.startswith(command) for command in self.commands]):
                return self.process_new_messages([message])

            return func(message, *args, **kwargs)

        return wrapper
