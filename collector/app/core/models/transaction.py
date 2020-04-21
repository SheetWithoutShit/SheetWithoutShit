"""Module that includes functionality to work with transaction data."""

import logging
from datetime import datetime

from asyncpg import exceptions

from core.database.queries import INSERT_TRANSACTION


LOG = logging.getLogger(__name__)


class Transaction:
    """Model that provides methods to work with transaction data."""

    costs_converter = 100.0

    def __init__(self, postgres=None, redis=None):
        """Initialize transaction instance with required clients."""
        self._postgres = postgres
        self._redis = redis

    async def _get_mcc(self, code):
        """Check if MCC exist in database, else return default value -1."""
        mcc = await self._redis.get("mcc", deserialize=True, default=[])
        if code not in mcc:
            return -1

        return code

    async def save_transaction(self, user_id, transaction):
        """Insert transaction element to postgres."""
        mcc = await self._get_mcc(transaction["mcc"])
        user_id = int(user_id)
        timestamp = datetime.fromtimestamp(transaction["timestamp"])
        amount = transaction["amount"] / self.costs_converter
        balance = transaction["balance"] / self.costs_converter
        cashback = transaction["cashback"] / self.costs_converter
        query_args = [
            transaction["id"], user_id, amount, balance,
            cashback, mcc, timestamp, transaction["info"],
        ]

        try:
            await self._postgres.execute(INSERT_TRANSACTION, *query_args)
        except exceptions.PostgresError as err:
            LOG.error(f"Could not insert transaction for user={user_id}: {transaction}. Error: {err}")
