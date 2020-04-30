"""This module provides interactions with monobank API."""


from core.http import HTTPRequest
from core.decorators import aioshield


MONOBANK_API = 'https://api.monobank.ua'


def parse_transaction_response(response):
    """Parse response from monobank API and return formatted transaction."""
    statement = response["data"]["statementItem"]
    return {
        "id": statement["id"],
        "amount": statement["amount"],
        "balance": statement["balance"],
        "cashback": statement["cashbackAmount"],
        "info": statement["description"],
        "mcc": statement["mcc"],
        "timestamp": statement["time"]
    }


class MonoBankAPI(HTTPRequest):
    """Class that provides HTTP API interactions with monobank API."""

    @staticmethod
    def format_headers(token):
        """Format headers with monobank token."""
        return {
            'X-Token': token
        }

    @aioshield
    async def set_webhook(self, token, base_url, user_id):
        """Set webhook by user's token and form webhook url based on collector's host and user's id."""
        webhook_url = f'{MONOBANK_API}/personal/webhook'
        headers = MonoBankAPI.format_headers(token)
        body = {'webHookUrl': f'{base_url}/receiver/{user_id}'}

        _, status = await self.post(url=webhook_url, headers=headers, body=body)
        return status == 200
