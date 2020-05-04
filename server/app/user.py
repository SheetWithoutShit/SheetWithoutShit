"""Module that includes functionality to work with user`s data."""

import logging

from asyncpg import exceptions


LOG = logging.getLogger(__name__)


CREATE_USER = """
    INSERT INTO "USER" (telegram_id, first_name, last_name)
         VALUES ($1, $2, $3);
"""

GET_USER = """
    SELECT * FROM "USER"
     WHERE telegram_id=$1
"""

UPDATE_SPREADSHEET_REFRESH_TOKEN = """
    UPDATE "USER"
       SET spreadsheet_refresh_token=$2
     WHERE telegram_id=$1
"""

UPDATE_MONOBANK_TOKEN = """
    UPDATE "USER"
       SET monobank_token=$2
     WHERE telegram_id=$1
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
            LOG.error("Couldn't create user=%s. Error: %s", telegram_id, err.message)

    async def retrieve_user(self, telegram_id):
        """Retrieve user from database by `telegram_id`."""
        try:
            record = await self._postgres.fetchone(GET_USER, telegram_id)
            return dict(record.items())
        except (exceptions.PostgresError, AttributeError) as err:
            LOG.error("Couldn't retrieve user=%s. Error: %s", telegram_id, err.message)

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

    async def update_monobank_token(self, telegram_id, token):
        """Update user`s monobank token."""
        try:
            return await self._postgres.execute(
                UPDATE_MONOBANK_TOKEN,
                telegram_id,
                token
            )
        except exceptions.PostgresError as err:
            LOG.error("Could not update user=%s monobank token. Error: %s", telegram_id, err.message)
