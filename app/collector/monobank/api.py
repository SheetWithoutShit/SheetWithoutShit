"""This module provides interactions with monobank API."""

from core.http import HTTPRequest

from collector.endpoints import MONOBANK_API


class MonoBankAPI(HTTPRequest):
    """Class that provides HTTP API interactions with monobank API."""

    def __init__(self, token):
        """Initialize user's token for further use."""
        super().__init__()
        self._token = token

    @property
    def headers(self):
        """Format headers with monobank token."""
        return {
            'X-Token': self._token
        }

    async def get_user_data(self):
        """Retrieve user's data by his token from monobank API"""
        user_data_url = f'{MONOBANK_API}/personal/client-info'

        response = await self.get(url=user_data_url, headers=self.headers)
        response_body = await response.json()
        return response.status, response_body

    async def set_webhook(self, base_url, user_id):
        """Set webhook by user's token and form webhook url based on collector's host and user's id."""
        webhook_url = f'{MONOBANK_API}/personal/webhook'
        body = {'webHookUrl': f'{base_url}/receiver/{user_id}'}

        response = await self.post(url=webhook_url, headers=self.headers, body=body)
        return response.status == 200

    async def get_payment_history(self, timestamp_from, timestamp_to=''):
        """Retrieve user's payment history between certain dates."""
        payment_history_url = f'{MONOBANK_API}/personal/statement/0/{timestamp_from}/{timestamp_to}'

        response = await self.get(url=payment_history_url, headers=self.headers)
        response_body = await response.json()
        return response.status, response_body
