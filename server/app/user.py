"""Module that includes functionality to work with user`s data."""

import logging

from asyncpg import exceptions


LOG = logging.getLogger(__name__)


CREATE_USER = """
    INSERT INTO "USER" (telegram_id, first_name, last_name)
         VALUES ($1, $2, $3);
"""

UPDATE_SPREADSHEET_REFRESH_TOKEN = """
    UPDATE "USER"
       SET spreadsheet_refresh_token=$2
     WHERE telegram_id=$1
"""


class User:
    """Model that provides methods to work with user`s data."""

    def __init__(self, postgres=None, redis=None):
        """Initialize user instance with required clients."""
        self._postgres = postgres
        self._redis = redis

    async def create_user(self, user):
        """Create new user in database."""
        telegram_id = user["telegram_id"]
        first_name = user.get("first_name")
        last_name = user.get("last_name")

        try:
            return await self._postgres.execute(
                CREATE_USER,
                telegram_id,
                first_name,
                last_name
            )
        except exceptions.PostgresError as err:
            LOG.error("Could not create user=%s. Error: %s", telegram_id, err.message)

    async def update_spreadsheet_token(self, telegram_id, refresh_token):
        """Update user`s spreadsheet refresh token."""
        try:
            return await self._postgres.execute(
                UPDATE_SPREADSHEET_REFRESH_TOKEN,
                telegram_id,
                refresh_token
            )
        except exceptions.PostgresError as err:
            LOG.error("Could not update user=%s spreadsheet token. Error: %s", telegram_id, err.message)
