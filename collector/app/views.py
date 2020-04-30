"""This module provides views for collector app."""

from aiohttp.web import RouteTableDef, json_response

from monobank import parse_transaction_response


routes = RouteTableDef()


@routes.post('/receiver/{user_id}')
async def receive_transaction(request):
    """Receive transaction from webhook and fill transaction data in DB and spreadsheets."""
    transaction = request.app["transaction"]
    user_id = request.match_info["user_id"]

    data = await request.json()
    transaction_item = parse_transaction_response(data)
    await transaction.save_transaction(user_id, transaction_item)

    return json_response(data={
        "message": "success",
        "user": user_id,
        "data": transaction_item
    })
