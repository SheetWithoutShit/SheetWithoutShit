"""This module provides views for collector app."""

import asyncio

from aiohttp.web import RouteTableDef, json_response

from decorators import permission_required
from models.monobank import Monobank


routes = RouteTableDef()


@routes.post(r"/receiver/{token}")
@permission_required
async def receive_transaction(request):
    """
    Receive transaction by webhook, insert transaction to appropriate
    table, notify user if notifications enabled and fill up spreadsheet.
    """
    transaction, user = request.app["transaction"], request.app["user"]

    data = await request.json()
    transaction_item = Monobank.parse_transaction_response(data)

    await asyncio.gather(
        transaction.save_transaction(request.user_id, transaction_item),
        user.notify_user(request.user_id, transaction_item)
    )

    return json_response(data={
        "message": "success",
        "user": request.user_id,
        "data": transaction_item
    })
