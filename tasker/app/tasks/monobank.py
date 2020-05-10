"""This module provides tasks related to user."""

import logging
from datetime import datetime

from asyncpg import exceptions


__all__ = ["save_monobank_info", "save_monobank_month_transactions"]


LOG = logging.getLogger(__name__)
MONOBANK_API = "https://api.monobank.ua"

UPDATE_USER_NAME_AND_TOKEN = """
    UPDATE "USER"
       SET first_name=$2, last_name=$3, monobank_token=$4
     WHERE telegram_id=$1
"""
INSERT_TRANSACTIONS = """
    INSERT INTO "TRANSACTION" (id, user_id, amount, balance, cashback, mcc, timestamp, info)
         VALUES ($1, $2, $3, $4, $5, $6, $7, $8);
"""


def _prepare_transactions(response, user_id, mcc_codes):
    """Parse response from monobank API and return formatted transaction."""
    transactions = []
    costs_converter = 100.0
    for transaction in response:
        transactions.append((
            transaction["id"],
            user_id,
            transaction["amount"] / costs_converter,
            transaction["balance"] / costs_converter,
            transaction["cashbackAmount"] / costs_converter,
            transaction["mcc"] if transaction["mcc"] in mcc_codes else -1,
            datetime.fromtimestamp(transaction["time"]),
            transaction["description"],
        ))

    return transactions


async def save_monobank_info(pools, telegram_id, token):
    """Retrieve user's data by his token from monobank API."""
    endpoint = f"{MONOBANK_API}/personal/client-info"
    headers = {"X-Token": token}

    http, postgres = pools["http"], pools["postgres"]
    response, status = await http.get(url=endpoint, headers=headers)
    if status != 200:
        LOG.error("Couldn't retrieve user`s=%s data from monobank. Error: %s", telegram_id, response)
        return

    last_name, first_name = response.get("name", "").split(" ")
    try:
        await postgres.execute(
            UPDATE_USER_NAME_AND_TOKEN,
            telegram_id,
            first_name,
            last_name,
            token
        )
    except exceptions.PostgresError as err:
        LOG.error("Could not update user=%s name. Error: %s", telegram_id, err)


async def save_monobank_month_transactions(pools, telegram_id, token):
    """
    Retrieve user's transactions by his token from monobank API
    that were made from the beginning of current month.
    """
    month_start_date = datetime.today().replace(day=1, hour=0, minute=0, second=0)
    month_start_timestamp = int(datetime.timestamp(month_start_date))
    endpoint = f"{MONOBANK_API}/personal/statement/0/{month_start_timestamp}"
    headers = {"X-Token": token}

    http, postgres, redis = pools["http"], pools["postgres"], pools["redis"]
    response, status = await http.get(url=endpoint, headers=headers)
    if status != 200:
        # TODO: test multiple requests for different token.
        LOG.error("Couldn't retrieve user`s=%s transactions from monobank. Error: %s", telegram_id, response)
        return

    mcc_codes = await redis.get("mcc", deserialize=True, default=[])
    transactions = _prepare_transactions(response, telegram_id, mcc_codes)
    try:
        await postgres.executemany(INSERT_TRANSACTIONS, transactions)
    except exceptions.PostgresError as err:
        LOG.error("Could not update user`s=%s transactions. Error: %s", telegram_id, err)
