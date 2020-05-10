"""This module provides views for collector app."""

import asyncio

from aiohttp.web import RouteTableDef, json_response

from monobank import parse_transaction_response


routes = RouteTableDef()


@routes.post(r"/receiver/{user_id:\d+}")
async def receive_transaction(request):
    """
    Receive transaction by webhook, insert transaction to appropriate
    table, notify user if notifications enabled and fill up spreadsheet.
    """
    transaction, user = request.app["transaction"], request.app["user"]
    user_id = int(request.match_info["user_id"])

    data = await request.json()
    transaction_item = parse_transaction_response(data)

    await asyncio.gather(
        transaction.save_transaction(user_id, transaction_item),
        user.notify_user(user_id, transaction_item)
    )

    return json_response(data={
        "message": "success",
        "user": user_id,
        "data": transaction_item
    })
