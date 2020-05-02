"""Module that includes functionality to work with user`s data."""

import logging

from asyncpg import exceptions


LOG = logging.getLogger(__name__)


CREATE_USER = """
    INSERT INTO "USER" (telegram_id)
         VALUES ($1);
"""


class User:
    """Model that provides methods to work with user`s data."""

    def __init__(self, postgres=None, redis=None):
        """Initialize user instance with required clients."""
        self._postgres = postgres
        self._redis = redis

    async def create_user(self, telegram_id):
        """Create new user in database."""
        try:
            return await self._postgres.execute(CREATE_USER, telegram_id)
        except exceptions.PostgresError as err:
            LOG.error("Could not create user=%s. Error: %s", telegram_id, err.message)
