"""This module provides main bot`s message handlers."""

import os
import logging

from handlers import bot

LOG = logging.getLogger("")
LOG_FORMAT = "%(asctime)s - %(levelname)s: %(name)s: %(message)s"


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


def main():
    """Create telegram bot and run it."""
    init_logging()

    LOG.info("Telegram bot was successfully initialized.")
    bot.polling(none_stop=True, interval=1)


if __name__ == '__main__':
    main()
