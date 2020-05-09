"""Module that includes functionality to work with transaction data."""

import logging
from datetime import datetime

from asyncpg import exceptions


LOG = logging.getLogger(__name__)


INSERT_TRANSACTION = """
    INSERT INTO "TRANSACTION" (id, user_id, amount, balance, cashback, mcc, timestamp, info)
         VALUES ($1, $2, $3, $4, $5, $6, $7, $8);
"""

SELECT_MCC_CODES = """
    SELECT code FROM "MCC";
"""


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
        """Insert transaction element to postgres initially formatting it."""
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
            LOG.error("Could not insert transaction for user=%s: %s. Error: %s", user_id, transaction, err)
