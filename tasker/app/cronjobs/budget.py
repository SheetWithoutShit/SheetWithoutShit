"""This module provides cron jobs that interact with budget data."""

import asyncio
import logging
import json

import asyncpg

from core.database.postgres import PoolManager as Postgres
from core.database.redis import PoolManager as Redis


__all__ = ["create_budgets"]


LOG = logging.getLogger(__name__)


INSERT_BUDGET = """
    INSERT INTO "BUDGET" (income, savings, user_id, year, month)
         SELECT income, 
                savings,
                $1, 
                EXTRACT(YEAR FROM CURRENT_TIMESTAMP),
                EXTRACT(MONTH FROM CURRENT_TIMESTAMP)
          FROM "BUDGET"
         WHERE user_id = $1
               and month = EXTRACT(MONTH FROM CURRENT_TIMESTAMP - interval '1 month')
               and year = EXTRACT(YEAR FROM CURRENT_TIMESTAMP - interval '1 month');
"""

GET_USERS = """
    SELECT telegram_id
      FROM "USER"
     WHERE spreadsheet_refresh_token IS NOT NULL
          and spreadsheet IS NOT NULL
"""


async def _create_sheet_tasks(user_ids):
    """Create future task for adding sheets to user`s spreadsheet."""
    redis = await Redis.create_connection()
    tasks_messages = [{"name": "create_sheet", "kwargs": {"telegram_id": user_id}} for user_id in user_ids]
    tasks_requests = [redis.execute("publish", "task", json.dumps(message)) for message in tasks_messages]
    await asyncio.gather(*tasks_requests)

    redis.close()
    await redis.wait_closed()


async def create_budgets():
    """
    Create budget item for each existing user with the same values
    as he has for previous month and publish task in order to create
    a new sheet to an existing user`s spreadsheet.
    Time: every first day of month at 00.00.
    """
    postgres = await Postgres.create_connection()

    try:
        records = await postgres.fetch(GET_USERS)
    except asyncpg.PostgresError as err:
        LOG.error("Couldn't select users. Error: %s", err)
        return

    try:
        await postgres.executemany(INSERT_BUDGET, [(x["telegram_id"], ) for x in records])
    except asyncpg.PostgresError as err:
        LOG.error("Couldn't create budgets for users. Error: %s", err)
        return
    finally:
        await postgres.close()

    users_ids = [x["telegram_id"] for x in records]
    await _create_sheet_tasks(users_ids)
    LOG.info("Budgets were successfully created for users: %s", users_ids)
