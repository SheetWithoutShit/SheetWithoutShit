"""This module provides interactions with monobank API."""

from core.http import HTTPRequest
from core.jwt import encode_jwt


MONOBANK_API = "https://api.monobank.ua"


class MonoBankAPI(HTTPRequest):
    """Class that provides HTTP API interactions with monobank API."""

    async def set_webhook(self, domain, user_id, token, secret_key):
        """
        Set webhook based on user's token and format webhook url
        based on collector's host and user's id.
        """
        webhook_url = f"{MONOBANK_API}/personal/webhook"
        headers = {"X-Token": token}

        user_token = encode_jwt({"user_id": user_id}, secret_key, exp_time=None).decode("utf-8")
        body = {"webHookUrl": f"{domain}/receiver/{user_token}"}

        response = await self.post(url=webhook_url, headers=headers, body=body)
        return response
