"""This module provides user`s views for server app."""

import asyncio
from datetime import datetime

from aiohttp import web

from utils.validators import validate_budget


user_routes = web.RouteTableDef()


@user_routes.view(r"/user/{telegram_id:\d+}")
class UserView(web.View):
    """Views to interact with user`s data."""

    async def get(self):
        """Retrieve user from database."""
        user = self.request.app["user"]

        user_info = await user.retrieve_user(self.request.user_id)
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
        data = await self.request.json()

        user = self.request.app["user"]
        created = await user.create_user(self.request.user_id, data)
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
        data = await self.request.json()

        user = self.request.app["user"]
        updated = await user.update_user(self.request.user_id, data)
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


@user_routes.view(r"/user/{telegram_id:\d+}/budget")
class UserBudgetView(web.View):
    """Views to interact with user budget data."""

    async def get(self):
        """Retrieve user`s monthly budget from database."""
        today = datetime.today()
        year = int(self.request.query.get("year") or today.year)
        month = int(self.request.query.get("month") or today.month)

        user = self.request.app["user"]
        month_budget = await user.retrieve_month_budget(self.request.user_id, year, month)
        if not month_budget:
            return web.json_response(
                data={
                    "success": False,
                    "message": "Couldn't retrieve user budget. Something went wrong. Try again, please."
                },
                status=400
            )

        return web.json_response(
            data={
                "success": True,
                "user": month_budget
            },
            status=200
        )

    async def put(self):
        """Update user`s budget in database."""
        data = await self.request.json()

        errors = validate_budget(data)
        if errors:
            return web.json_response(
                data={
                    "success": False,
                    "message": f"Provided incorrect input: {errors}."
                },
                status=400
            )

        user = self.request.app["user"]
        updated = await user.update_budget(self.request.user_id, data)
        if not updated:
            return web.json_response(
                data={
                    "success": False,
                    "message": "The budget wasn't updated. Something went wrong. Try again, please."
                },
                status=400
            )

        return web.json_response(
            data={
                "success": True,
                "message": "The budget was successfully updated."
            },
            status=200
        )


@user_routes.view(r"/user/{telegram_id:\d+}/spreadsheet")
class SpreadsheetView(web.View):
    """View to interact with user spreadsheet`s data"""

    async def post(self):
        """Update user`s spreadsheet refresh token."""
        data = await self.request.json()

        auth_code = data.get("auth_code")
        if not auth_code:
            return web.json_response(
                data={
                    "success": False,
                    "message": "Required field `auth_code` weren't provided."
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
        updated = await user.update_user(
            self.request.user_id,
            {"spreadsheet_refresh_token": spreadsheet_credentials["refresh_token"]}
        )
        if not updated:
            return web.json_response(
                data={
                    "success": False,
                    "message": "The spreadsheet token wasn't created. Something went wrong. Try again, please."
                },
                status=400
            )

        redis = self.request.app["redis"]
        await redis.publish("task", {"name": "create_spreadsheet", "kwargs": {"telegram_id": self.request.user_id}})

        return web.json_response(
            data={
                "success": True,
                "message": "The spreadsheet account was registered successfully."
            },
            status=200
        )


@user_routes.view(r"/user/{telegram_id:\d+}/monobank")
class MonobankView(web.View):
    """View to interact with monobank data."""

    async def post(self):
        """Update user`s monobank access token."""
        data = await self.request.json()

        token = data.get("token")
        if not token:
            return web.json_response(
                data={
                    "success": False,
                    "message": "Required field `token` wasn't provided."
                },
                status=400
            )

        ngrok_domain = self.request.app["constants"]["NGROK_DOMAIN"]
        secret_key = self.request.app["constants"]["SECRET_KEY"]
        monobank = self.request.app["monobank"]
        _, status = await monobank.set_webhook(ngrok_domain, self.request.user_id, token, secret_key)
        if status != 200:
            return web.json_response(
                data={"message": "The `token` isn't correct."},
                status=400
            )

        redis = self.request.app["redis"]
        task_kwargs = {"telegram_id": self.request.user_id, "token": token}
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
