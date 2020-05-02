"""This module provides task app initialization."""

import os
import argparse
import asyncio
import logging

from subscriber import RedisSubscriber


LOG = logging.getLogger("")
LOG_FORMAT = "%(asctime)s - %(levelname)s: %(name)s: %(message)s"


def init_logging():
    """Initialize stream and file logger if it is available."""
    logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)

    log_dir = os.environ.get("LOG_DIR")
    log_filepath = f"{log_dir}/server.log"
    if log_dir and os.path.isfile(log_filepath) and os.access(log_filepath, os.W_OK):
        formatter = logging.Formatter(LOG_FORMAT)
        file_handler = logging.FileHandler(log_filepath)
        file_handler.setFormatter(formatter)
        logging.getLogger("").addHandler(file_handler)


async def main(channel_name):
    """Initialize redis subscriber and run it."""
    subscriber = await RedisSubscriber.create()
    await subscriber.subscribe(channel_name)
    LOG.info("Subscriber=%s reading channel: <%s>", subscriber.pid, subscriber.channel_name)

    await subscriber.read()
    await subscriber.close()

    LOG.info("Subscriber=%s gracefully closed.", subscriber.pid)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", dest="channel_name", required=True, help="Name of channel for subscribing.")
    args = parser.parse_args()

    init_logging()

    asyncio.run(main(args.channel_name))
