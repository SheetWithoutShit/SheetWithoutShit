"""This module provides views for server app."""

import asyncio

from aiohttp import web


routes = web.RouteTableDef()


@routes.view(r"/user/{telegram_id:\d+}")
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


@routes.view('/spreadsheet')
class SpreadsheetView(web.View):
    """View to interact with spreadsheet`s data"""

    async def get(self):
        """
        Return formatted authorization url in order to
        get access to user`s google spreadsheet account.
        """
        spreadsheet_auth = self.request.app["spreadsheet_auth"]
        spreadsheet_auth_url = spreadsheet_auth.auth_url
        return web.json_response(
            data={
                "success": True,
                "auth_url": spreadsheet_auth_url
            },
            status=200
        )

    async def post(self):
        """Update user`s spreadsheet refresh token."""
        data = await self.request.json()

        telegram_id, auth_code = data.get("telegram_id"), data.get("auth_code")
        if not auth_code or not telegram_id:
            return web.json_response(
                data={
                    "success": False,
                    "message": "Required fields `auth_code` and `telegram_id` weren't provided."
                },
                status=400
            )

        spreadsheet_auth = self.request.app["spreadsheet_auth"]
        spreadsheet_credentials, status = await spreadsheet_auth.fetch_credentials(auth_code)
        if status != 200:
            return web.json_response(
                data={
                    "success": False,
                    "message": "The `auth_code` isn't correct."
                },
                status=400
            )

        user = self.request.app["user"]
        updated = await user.update_spreadsheet_token(
            telegram_id,
            spreadsheet_credentials["refresh_token"]
        )
        if not updated:
            return web.json_response(
                data={
                    "success": False,
                    "message": "The spreadsheet token wasn't created. Something went wrong. Try again, please."
                },
                status=400
            )

        return web.json_response(
            data={
                "success": True,
                "message": "The spreadsheet account was registered successfully."
            },
            status=200
        )


@routes.view('/monobank')
class MonobankView(web.View):
    """View to interact with monobank data."""

    async def post(self):
        """Update user`s monobank access token."""
        data = await self.request.json()

        telegram_id, token = data.get("telegram_id"), data.get("token")
        if not token or not telegram_id:
            return web.json_response(
                data={
                    "success": False,
                    "message": "Required fields `token` and `telegram_id` weren't provided."
                },
                status=400
            )

        ngrok_domain = self.request.app["constants"]["NGROK_DOMAIN"]
        monobank = self.request.app["monobank"]
        _, status = await monobank.set_webhook(ngrok_domain, telegram_id, token)
        if status != 200:
            return web.json_response(
                data={"message": "The `token` isn't correct."},
                status=400
            )

        redis = self.request.app["redis"]
        task_kwargs = {"telegram_id": telegram_id, "token": token}
        await asyncio.gather(
            redis.publish("task", {"name": "save_monobank_info", "kwargs": task_kwargs}),
            redis.publish("task", {"name": "save_monobank_month_transactions", "kwargs": task_kwargs})
        )

        return web.json_response(
            data={
                "success": True,
                "message": "The monobank account was registered successfully."
            },
            status=200
        )
