"""This module provides interactions with google spreadsheet API and auth."""

import os

from core.http import HTTPRequest


SPREADSHEET_API = "https://sheets.googleapis.com/v4/spreadsheets"
SPREADSHEET_TOKEN = "https://oauth2.googleapis.com/token"
SPREADSHEET_OAUTH = "https://accounts.google.com/o/oauth2/v2/auth"
SPREADSHEET_SCOPE = "https://www.googleapis.com/auth/spreadsheets"


class SpreadsheetAuth(HTTPRequest):
    """Class that provides google auth interactions in spreadsheet scope."""

    def __init__(self):
        """Initialize client for google spreadsheet auth."""
        super().__init__()
        self.redirect_uri = os.environ["SPREADSHEET_REDIRECT_URI"]
        self.client_id = os.environ["SPREADSHEET_CLIENT_ID"]
        self.client_secret = os.environ["SPREADSHEET_CLIENT_SECRET"]

    async def refresh_credentials(self, refresh_token):
        """
        Return refreshed access token for user.
        Response contains the following information:
        new access token, expires token time scope and token type.
        """
        payload = {
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
            "client_secret": self.client_secret,
            "client_id": self.client_id
        }
        credentials = await self.post(SPREADSHEET_TOKEN, body=payload)
        return credentials


class SpreadsheetAPI(HTTPRequest):
    """
    Class that provides HTTP API interactions with google spreadsheet.
    As refers to a group of cells in the spreadsheet use A1 notation.
    In order to specify the values range use A1 notation.
    """

    @staticmethod
    def format_headers(token):
        """
        Return formatted authorization headers for further
        interactions with spreadsheet api.
        """
        return {
            "Authorization": f"Bearer {token}"
        }

    async def update_sheet(self, token, spreadsheet_id, modifications, input_option):
        """Set values in one or more ranges of a spreadsheet."""
        url = f'{SPREADSHEET_API}/{spreadsheet_id}/values:batchUpdate'
        body = {"data": modifications, "valueInputOption": input_option}
        headers = SpreadsheetAPI.format_headers(token)

        response = await self.post(url, headers, body)
        return response
