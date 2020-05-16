"""This module provides cronner functionality."""

import asyncio
import argparse
import logging

import cronjobs

from main import init_logging


LOG = logging.getLogger(__name__)


async def main(task_name):
    """Gather task by provided name and run it."""
    task = getattr(cronjobs, task_name, None)
    if not task:
        LOG.error("There is not such task: %s", task_name)
        return

    await task()


if __name__ == '__main__':
    init_logging("cronner")

    parser = argparse.ArgumentParser()
    parser.add_argument("--task", required=True, help="The name of cron task.")
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args.task))
