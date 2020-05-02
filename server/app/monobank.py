"""This module provides interactions with monobank API."""

import os

from core.http import HTTPRequest
from core.decorators import aioshield


MONOBANK_API = "https://api.monobank.ua"


class MonoBankAPI(HTTPRequest):
    """Class that provides HTTP API interactions with monobank API."""

    @staticmethod
    def format_headers(token):
        """Format headers with monobank token."""
        return {
            "X-Token": token
        }

    async def get_user_info(self, token):
        """Retrieve user's data by his token from monobank API."""
        user_info_url = f"{MONOBANK_API}/personal/client-info"
        headers = MonoBankAPI.format_headers(token)
        response = await self.get(url=user_info_url, headers=headers)

        return response

    @aioshield
    async def set_webhook(self, user_id, token):
        """
        Set webhook based on user's token and format webhook url
        based on collector's host and user's id.
        """
        webhook_url = f"{MONOBANK_API}/personal/webhook"
        headers = MonoBankAPI.format_headers(token)

        domain = os.environ["NGROK_DOMAIN"]
        body = {"webHookUrl": f"{domain}/receiver/{user_id}"}

        response = await self.post(url=webhook_url, headers=headers, body=body)
        return response
