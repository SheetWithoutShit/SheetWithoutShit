"""This module provides interactions with monobank data."""


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
