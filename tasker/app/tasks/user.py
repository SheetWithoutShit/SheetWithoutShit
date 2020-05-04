"""This module provides tasks related to user."""

import logging

from asyncpg import exceptions


__all__ = ["save_user_monobank_info"]


LOG = logging.getLogger(__name__)

UPDATE_USER_NAME = """
    UPDATE "USER"
       SET first_name=$2, last_name=$3, monobank_token=$4
     WHERE telegram_id=$1
"""


async def save_user_monobank_info(pools, telegram_id, token):
    """Retrieve user's data by his token from monobank API."""
    endpoint = "https://api.monobank.ua/personal/client-info"
    headers = {"X-Token": token}

    http, postgres = pools["http"], pools["postgres"]
    response, status = await http.get(url=endpoint, headers=headers)
    if status != 200:
        LOG.error("Couldn't retrieve user`s=%s data from monobank. Error: %s", telegram_id, response)
        return

    last_name, first_name = response.get("name", "").split(" ")
    try:
        await postgres.execute(
            UPDATE_USER_NAME,
            telegram_id,
            first_name,
            last_name,
            token
        )
    except exceptions.PostgresError as err:
        LOG.error("Could not update user=%s name. Error: %s", telegram_id, err.message)
