"""This module provides cron jobs that interact with budget data."""

import logging

import asyncpg

from core.database.postgres import PoolManager as Postgres


__all__ = ["create_budgets"]


LOG = logging.getLogger(__name__)


INSERT_BUDGET = """
    INSERT INTO "BUDGET" (income, savings, spreadsheet, user_id, year, month)
         SELECT income, 
                savings,
                spreadsheet,
                $1, 
                EXTRACT(YEAR FROM CURRENT_TIMESTAMP),
                EXTRACT(MONTH FROM CURRENT_TIMESTAMP)
          FROM "BUDGET"
         WHERE user_id = $1 
               and month = EXTRACT(MONTH FROM CURRENT_TIMESTAMP - interval '1 month')
               and year = EXTRACT(YEAR FROM CURRENT_TIMESTAMP - interval '1 month');
"""

GET_USERS = """
    SELECT user_table.telegram_id, budget.spreadsheet
      FROM "USER" as user_table
      LEFT JOIN "BUDGET" as budget ON user_table.telegram_id=budget.user_id
     WHERE user_table.spreadsheet_refresh_token IS NOT NULL
           and budget.year = EXTRACT(YEAR FROM CURRENT_TIMESTAMP - interval '1 month')
           and budget.month = EXTRACT(MONTH FROM CURRENT_TIMESTAMP - interval '1 month');
"""


async def create_budgets():
    """
    Create budget item for each existing user with
    the same values as he has for previous month.
    Time: every first day of month at 00.00.
    """
    postgres = await Postgres.create_connection()

    try:
        records = await postgres.fetch(GET_USERS)
    except asyncpg.PostgresError as err:
        LOG.error("Couldn't select users. Error: %s", err)
        return

    users_ids = [(x["telegram_id"], ) for x in records]
    try:
        await postgres.executemany(INSERT_BUDGET, users_ids)
    except asyncpg.PostgresError as err:
        LOG.error("Couldn't create budgets for users. Error: %s", err)
        return

    LOG.info("Budgets were successfully created for users: %s", users_ids)
    # TODO: publish tasks to create sheets for user`s with spreadsheet
