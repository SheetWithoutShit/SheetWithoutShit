"""Module that includes functionality to work with user`s data."""

import logging

from asyncpg import exceptions


LOG = logging.getLogger(__name__)


CREATE_USER = """
    INSERT INTO "USER" (telegram_id, first_name, last_name)
         VALUES ($1, $2, $3);
"""

GET_USER = """
    SELECT user_table.*, budget.savings
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

UPDATE_SAVINGS = """
    UPDATE "BUDGET"
       SET savings=$2
     WHERE user_id = $1
           and year = EXTRACT(YEAR FROM CURRENT_TIMESTAMP)
           and month = EXTRACT(MONTH FROM CURRENT_TIMESTAMP)
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

    async def update_savings(self, telegram_id, savings):
        """Update user`s budget savings for the current month."""
        try:
            return await self._postgres.execute(UPDATE_SAVINGS, telegram_id, savings)
        except exceptions.PostgresError as err:
            LOG.error("Could not update user=%s savings. Error: %s", telegram_id, err)
