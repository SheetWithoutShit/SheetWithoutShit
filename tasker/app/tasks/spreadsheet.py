"""This module provides tasks related to interactions with spreadsheet api."""

import os
import logging
from datetime import datetime


__all__ = ["create_spreadsheet"]

LOG = logging.getLogger(__name__)

SPREADSHEET_API = "https://sheets.googleapis.com/v4/spreadsheets"
SPREADSHEET_TOKEN_API = "https://oauth2.googleapis.com/token"
SPREADSHEET_CLIENT_ID = os.environ["SPREADSHEET_CLIENT_ID"]
SPREADSHEET_CLIENT_SECRET = os.environ["SPREADSHEET_CLIENT_SECRET"]

GET_SPREADSHEET_TOKENS = """
    SELECT spreadsheet_refresh_token
      FROM "USER"
     WHERE telegram_id = $1;
"""

UPDATE_SPREADSHEET_ID = """
    UPDATE "BUDGET"
       SET spreadsheet = $1
     WHERE user_id = $2
"""


def _get_sheet_properties():
    """Return formatted properties for a new sheet."""
    today = datetime.today()
    title = f"{today.month}.{today.year}"
    sheet_id = f"{today.month}{today.year}"
    return {
        "title": title,
        "sheetId": int(sheet_id),
        "index": 0
    }


async def _refresh_credentials(http_client, refresh_token):
    """Send request in order to refresh credentials to spreadsheet account."""
    refresh_credentials_payload = {
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
        "client_secret": SPREADSHEET_CLIENT_SECRET,
        "client_id": SPREADSHEET_CLIENT_ID
    }
    credentials = await http_client.post(SPREADSHEET_TOKEN_API, body=refresh_credentials_payload)
    return credentials


async def create_spreadsheet(pools, telegram_id):
    """Create spreadsheet for user in google spreadsheet account."""
    http, postgres = pools["http"], pools["postgres"]

    record = await postgres.fetchone(GET_SPREADSHEET_TOKENS, telegram_id)

    credentials, status = await _refresh_credentials(http, record["spreadsheet_refresh_token"])
    if status != 200:
        LOG.error("Couldn't refresh credentials for user=%s. Error: %s", telegram_id, credentials)
        return

    headers = {"Authorization": f"Bearer {credentials['access_token']}"}
    body = {
        "properties": {"title": "Sheet Without Shit"},
        "sheets": [{"properties": _get_sheet_properties()}]
    }

    response, status = await http.post(url=SPREADSHEET_API, headers=headers, body=body)
    if status != 200:
        LOG.error("Couldn't create spreadsheet for user=%s. Error: %s", telegram_id, response)
        return

    await postgres.execute(UPDATE_SPREADSHEET_ID, response["spreadsheetId"], telegram_id)

    # TODO: create task to update sheet with values
    LOG.info("Spreadsheet was successfully created for user=%s", telegram_id)
