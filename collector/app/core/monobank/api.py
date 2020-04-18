"""This module provides interactions with monobank API."""

from core.http import HTTPRequest
from core.decorators import aioshield


MONOBANK_API = 'https://api.monobank.ua'


class MonoBankAPI(HTTPRequest):
    """Class that provides HTTP API interactions with monobank API."""

    @staticmethod
    def format_headers(token):
        """Format headers with monobank token."""
        return {
            'X-Token': token
        }

    async def get_user_data(self, token):
        """Retrieve user's data by his token from monobank API"""
        user_data_url = f'{MONOBANK_API}/personal/client-info'
        headers = MonoBankAPI.format_headers(token)

        response = await self.get(url=user_data_url, headers=headers)
        return response

    @aioshield
    async def set_webhook(self, token, base_url, user_id):
        """Set webhook by user's token and form webhook url based on collector's host and user's id."""
        webhook_url = f'{MONOBANK_API}/personal/webhook'
        headers = MonoBankAPI.format_headers(token)
        body = {'webHookUrl': f'{base_url}/receiver/{user_id}'}

        _, status = await self.post(url=webhook_url, headers=headers, body=body)
        return status == 200

    async def get_payment_history(self, token, timestamp_from, timestamp_to=''):
        """Retrieve user's payment history between certain dates."""
        payment_history_url = f'{MONOBANK_API}/personal/statement/0/{timestamp_from}/{timestamp_to}'
        headers = MonoBankAPI.format_headers(token)

        response = await self.get(url=payment_history_url, headers=headers)
        return response
