"""This module provides task app initialization."""

import os
import asyncio
import logging

from scheduler import TaskScheduler
from subscriber import TaskReader


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


async def main():
    """Initialize tasker with required entities.
        * redis subscriber (TaskReader)
        * task executor (TaskScheduler)
    """

    reader = await TaskReader.create()
    scheduler = await TaskScheduler.create()

    await reader.subscribe()
    await reader.read(scheduler)

    await reader.close()
    await scheduler.close()

    LOG.debug("Tasker has successfully closed.")


if __name__ == '__main__':
    init_logging()
    asyncio.run(main())
