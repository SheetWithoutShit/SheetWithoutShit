"""This module provides user`s views for server app."""

from aiohttp import web


user_routes = web.RouteTableDef()


@user_routes.view(r"/user/{telegram_id:\d+}")
class UserView(web.View):
    """Views to interact with user`s data."""

    async def get(self):
        """Retrieve user from database."""
        telegram_id = int(self.request.match_info["telegram_id"])
        user = self.request.app["user"]

        user_info = await user.retrieve_user(telegram_id)
        if not user_info:
            return web.json_response(
                data={
                    "success": False,
                    "message": "Couldn't retrieve user. Something went wrong. Try again, please."
                },
                status=400
            )

        return web.json_response(
            data={
                "success": True,
                "user": user_info
            },
            status=200
        )

    async def post(self):
        """Create new user in database."""
        telegram_id = int(self.request.match_info["telegram_id"])
        data = await self.request.json()

        user = self.request.app["user"]
        created = await user.create_user(telegram_id, data)
        if not created:
            return web.json_response(
                data={
                    "success": False,
                    "message": "The user wasn't created. Something went wrong. Try again, please."
                },
                status=400
            )

        return web.json_response(
            data={
                "success": True,
                "message": "The user was successfully created."
            },
            status=200
        )

    async def put(self):
        """Update user`s data in database."""
        telegram_id = int(self.request.match_info["telegram_id"])
        data = await self.request.json()

        user = self.request.app["user"]
        updated = await user.update_user(telegram_id, data)
        if not updated:
            return web.json_response(
                data={
                    "success": False,
                    "message": "The user wasn't updated. Something went wrong. Try again, please."
                },
                status=400
            )

        return web.json_response(
            data={
                "success": True,
                "message": "The user was successfully updated."
            },
            status=200
        )


@user_routes.put(r"/user/{telegram_id:\d+}/savings")
async def savings_update_handler(request):
    """Update user`s savings in database."""
    telegram_id = int(request.match_info["telegram_id"])
    data = await request.json()

    savings = data.get("savings")
    if not savings or not 0 <= savings <= 100:
        return web.json_response(
            data={
                "success": False,
                "message": "Required fields `savings` wasn't provided or incorrect."
            },
            status=400
        )

    user = request.app["user"]
    updated = await user.update_savings(telegram_id, savings)
    if not updated:
        return web.json_response(
            data={
                "success": False,
                "message": "The savings wasn't updated. Something went wrong. Try again, please."
            },
            status=400
        )

    return web.json_response(
        data={
            "success": True,
            "message": "The savings was successfully updated."
        },
        status=200
    )
