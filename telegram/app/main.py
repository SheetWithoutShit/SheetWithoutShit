"""This module provides main bot`s message handlers."""

import os
import logging

from telebot import TeleBot

import messages


LOG = logging.getLogger("")
LOG_FORMAT = "%(asctime)s - %(levelname)s: %(name)s: %(message)s"
BOT = TeleBot(os.environ["TELEGRAM_BOT_TOKEN"])


def init_logging():
    """Initialize stream and file logger if it is available."""
    logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)

    log_dir = os.environ.get("LOG_DIR")
    log_filepath = f'{log_dir}/telegram.log'
    if log_dir and os.path.exists(log_filepath) and os.access(log_filepath, os.W_OK):
        formatter = logging.Formatter(LOG_FORMAT)
        file_handler = logging.FileHandler(log_filepath)
        file_handler.setFormatter(formatter)
        logging.getLogger("").addHandler(file_handler)


@BOT.message_handler(commands=['help'])
def handle_help_command(message):
    """Send help information to user."""
    BOT.send_message(message.from_user.id, messages.HELP_TEXT)


@BOT.message_handler(commands=['start'])
def handle_start_command(message):
    """Send start steps to user."""
    BOT.send_message(message.from_user.id, messages.START_TEXT)


def main():
    """Create telegram bot and run it."""
    init_logging()
    BOT.polling(none_stop=True, interval=1)


if __name__ == '__main__':
    main()
