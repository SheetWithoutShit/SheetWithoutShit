"""This module provides interactions with monobank API."""

from core.http import HTTPRequest
from core.decorators import aioshield


MONOBANK_API = "https://api.monobank.ua"


class MonoBankAPI(HTTPRequest):
    """Class that provides HTTP API interactions with monobank API."""

    @aioshield
    async def set_webhook(self, domain, user_id, token):
        """
        Set webhook based on user's token and format webhook url
        based on collector's host and user's id.
        """
        webhook_url = f"{MONOBANK_API}/personal/webhook"
        headers = {"X-Token": token}

        body = {"webHookUrl": f"{domain}/receiver/{user_id}"}

        response = await self.post(url=webhook_url, headers=headers, body=body)
        return response
