"""This module provides task app initialization."""

import os
import argparse
import asyncio
import logging

import tasks
from subscriber import TaskReader
from scheduler import TaskScheduler


LOG = logging.getLogger("")
LOG_FORMAT = "%(asctime)s - %(levelname)s: %(name)s: %(message)s"


def init_logging():
    """
    Initialize logging stream with debug level to console and
    create file logger with info level if permission to file allowed.
    """
    logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)

    log_dir = os.environ.get("LOG_DIR")
    log_filepath = f"{log_dir}/server.log"
    if log_dir and os.path.isfile(log_filepath) and os.access(log_filepath, os.W_OK):
        formatter = logging.Formatter(LOG_FORMAT)
        file_handler = logging.FileHandler(log_filepath)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logging.getLogger("").addHandler(file_handler)


async def main(channel_name, limit, pending_limit):
    """
    Initialize tasker application with required entities.
        * redis subscriber (TaskReader)
        * task executor (TaskScheduler)
    """
    pid = os.getpid()

    reader = await TaskReader.create(pid)
    scheduler = await TaskScheduler.create(pid, tasks, limit, pending_limit)

    await reader.subscribe(channel_name)
    await reader.read(scheduler)

    await reader.close()
    await scheduler.close()

    LOG.debug("Tasker %s has successfully closed.", pid)


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
