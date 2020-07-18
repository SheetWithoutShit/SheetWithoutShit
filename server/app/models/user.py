"""Module that includes functionality to work with user`s data."""

import logging

from asyncpg import exceptions


LOG = logging.getLogger(__name__)


CREATE_USER = """
    INSERT INTO "USER" (telegram_id, first_name, last_name)
    VALUES ($1, $2, $3);
"""

GET_USER = """
    SELECT user_table.*, budget.savings, budget.income::varchar
    FROM "USER" as user_table
    LEFT JOIN "BUDGET" as budget ON user_table.telegram_id=budget.user_id
    WHERE telegram_id=$1
        and budget.year = EXTRACT(YEAR FROM CURRENT_TIMESTAMP)
        and budget.month = EXTRACT(MONTH FROM CURRENT_TIMESTAMP)
"""

UPDATE_USER = """
    UPDATE "USER"
    SET first_name = COALESCE($2, first_name),
        last_name = COALESCE($3, last_name),
        notifications_enabled = COALESCE($4, notifications_enabled),
        monobank_token= COALESCE($5, monobank_token),
        spreadsheet = COALESCE($6, spreadsheet),
        spreadsheet_refresh_token= COALESCE($7, spreadsheet_refresh_token)
    WHERE telegram_id=$1
"""

UPDATE_BUDGET = """
    UPDATE "BUDGET"
    SET savings = COALESCE($2, savings),
        income = COALESCE($3, income)
    WHERE user_id = $1
        and year = EXTRACT(YEAR FROM CURRENT_TIMESTAMP)
        and month = EXTRACT(MONTH FROM CURRENT_TIMESTAMP)
"""

GET_MONTH_BUDGET = """
    SELECT mcc, mcc_table.category, mcc_table.info, ABS(SUM(amount))::varchar as amount
    FROM "TRANSACTION"
    LEFT JOIN "MCC" as mcc_table on mcc=code
    WHERE user_id=$1
        and amount >= 0
        and EXTRACT(YEAR FROM timestamp) = $2
        and EXTRACT(MONTH FROM timestamp) = $3
    GROUP BY mcc, mcc_table.category, mcc_table.info
"""


class User:
    """Model that provides methods to work with user`s data."""

    def __init__(self, postgres=None, redis=None):
        """Initialize user instance with required clients."""
        self._postgres = postgres
        self._redis = redis

    async def create_user(self, telegram_id, user):
        """Create new user in database."""
        first_name = user.get("first_name")
        last_name = user.get("last_name")

        try:
            return await self._postgres.execute(
                CREATE_USER,
                int(telegram_id),
                first_name,
                last_name
            )
        except (exceptions.PostgresError, ValueError) as err:
            LOG.error("Couldn't create user=%s. Error: %s", telegram_id, err)

    async def retrieve_user(self, telegram_id):
        """Retrieve user from database by `telegram_id`."""
        try:
            record = await self._postgres.fetchone(GET_USER, telegram_id)
            return dict(record.items())
        except exceptions.PostgresError as err:
            LOG.error("Couldn't retrieve user=%s. Error: %s", telegram_id, err)
        except AttributeError:
            LOG.error("User=%s doesn't not exist.", telegram_id)

    async def update_user(self, telegram_id, data):
        """Update user`s data in database by `telegram_id`."""
        update_args = (
            data.get("first_name"),
            data.get("last_name"),
            data.get("notifications_enabled"),
            data.get("monobank_token"),
            data.get("spreadsheet"),
            data.get("spreadsheet_refresh_token")
        )
        try:
            return await self._postgres.execute(UPDATE_USER, telegram_id, *update_args)
        except exceptions.PostgresError as err:
            LOG.error("Could not update user=%s spreadsheet token. Error: %s", telegram_id, err)

    async def update_budget(self, telegram_id, data):
        """Update user`s budget for the current month."""
        update_args = (
            data.get("savings"),
            data.get("income")
        )
        try:
            return await self._postgres.execute(UPDATE_BUDGET, telegram_id, *update_args)
        except exceptions.PostgresError as err:
            LOG.error("Could not update user=%s budget. Error: %s", telegram_id, err)

    async def retrieve_month_budget(self, telegram_id, year, month):
        """Retrieve user budget information for specific month."""
        try:
            records = await self._postgres.fetch(GET_MONTH_BUDGET, telegram_id, year, month)
            return [dict(x) for x in records]
        except exceptions.PostgresError as err:
            LOG.error("Couldn't retrieve budget for user=%s. Error: %s", telegram_id, err)
