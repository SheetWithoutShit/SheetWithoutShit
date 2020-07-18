"""This module provides services views for server app."""

from aiohttp import web


services_routes = web.RouteTableDef()


@services_routes.view('/spreadsheet')
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
