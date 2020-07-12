"""This module provides cron jobs that interact with reports."""

import asyncio
import logging
import json

import asyncpg

from core.database.postgres import PoolManager as Postgres
from core.database.redis import PoolManager as Redis


__all__ = ["daily_report"]


LOG = logging.getLogger(__name__)


GET_USERS = """
    SELECT telegram_id
    FROM "USER"
"""


async def daily_report():
    """
    Create tasks for sending daily budget report for every registered
    user in the database. Reports contain information about spent and
    saved costs.
    Time: every day at very beginning (00:00).
    """
    postgres = await Postgres.create_connection()
    try:
        records = await postgres.fetch(GET_USERS)
    except asyncpg.PostgresError as err:
        LOG.error("Couldn't select users. Error: %s", err)
        return

    redis = await Redis.create_connection()
    tasks_messages = [{"name": "send_daily_report", "kwargs": {"user_id": x["telegram_id"]}} for x in records]
    tasks_requests = [redis.execute("publish", "task", json.dumps(message)) for message in tasks_messages]
    await asyncio.gather(*tasks_requests)

    redis.close()
    await redis.wait_closed()
    LOG.info("Daily report tasks were created for %s users.", len(tasks_requests))
