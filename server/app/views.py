"""This module provides views for server app."""

from aiohttp.web import RouteTableDef, json_response


routes = RouteTableDef()


@routes.post('/user')
async def user_register(request):
    """Create new user to database."""
    data = await request.json()
    user = request.app["user"]

    telegram_id = data.get("telegram_id")
    if not telegram_id:
        return json_response(
            data={"message": "The field `telegram_id` wasn't provided"},
            status=400
        )

    created = await user.create_user(telegram_id)
    if not created:
        return json_response(
            data={"message": "The user wasn't created. Something went wrong. Try again, please."},
            status=400
        )

    return json_response(
        data={"message": "The user was successfully created."},
        status=200
    )
