"""This module provides task app initialization."""

import os
import argparse
import asyncio
import logging

from subscriber import RedisSubscriber
from scheduler import TaskScheduler


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


async def main(channel_name, limit, pending_limit):
    """Initialize redis subscriber and run it."""
    pid = os.getpid()

    subscriber = await RedisSubscriber.create(pid)
    scheduler = await TaskScheduler.create(pid, limit, pending_limit)

    await subscriber.subscribe(channel_name)
    LOG.info("TaskManager=%s reading channel: <%s>", pid, subscriber.channel_name)

    await subscriber.read(scheduler)

    await subscriber.close()
    await scheduler.close()

    LOG.info("TaskManager=%s is closed.", pid)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", dest="channel_name", required=True, help="Name of channel for subscribing.")
    parser.add_argument("--tasks-limit", dest="limit", help="Limit tasks spawned by scheduler.")
    parser.add_argument("--pending-limit", dest="pending_limit", default=0, help="Limit pending tasks.")
    args = parser.parse_args()

    init_logging()

    asyncio.run(
        main(args.channel_name, args.limit, args.pending_limit)
    )
