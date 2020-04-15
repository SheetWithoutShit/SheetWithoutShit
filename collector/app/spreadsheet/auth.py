"""This module provides interactions with google spreadsheet auth."""

import os

from core.http import HTTPRequest
from utils.request import format_params

from endpoints import (
    SPREADSHEET_OAUTH,
    SPREADSHEET_SCOPE,
    SPREADSHEET_TOKEN
)


class SpreadsheetAuth(HTTPRequest):
    """Class that provides google auth interactions in spreadsheet scope."""

    def __init__(self):
        """Initialize client for google spreadsheet auth."""
        super().__init__()
        # TODO: load configs from app['config']
        self.redirect_uri = os.environ["SPREADSHEET_REDIRECT_URI"]
        self.client_id = os.environ["SPREADSHEET_CLIENT_ID"]
        self.client_secret = os.environ["SPREADSHEET_CLIENT_SECRET"]

    @property
    def auth_url(self):
        """
        Returns formatted URL for further authorizing user
        in the spreadsheet scope.
        """
        params = {
            "response_type": "code",
            "scope": SPREADSHEET_SCOPE,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
        }
        return f'{SPREADSHEET_OAUTH}?{format_params(params)}'

    async def fetch_credentials(self, auth_code):
        """
        Return received user credentials for provided auth code.
        Response contains the following information: access token,
        expires token time, refresh token, scope and token type.
        """
        payload = {
            "code": auth_code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        credentials = await self.post(SPREADSHEET_TOKEN, body=payload)
        return credentials

    async def refresh_credentials(self, refresh_token):
        """
        Return refreshed access token for user. Response contains
        the following information: new access token, expires token time
        scope and token type.
        """
        payload = {
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
            "client_secret": self.client_secret,
            "client_id": self.client_id
        }
        credentials = await self.post(SPREADSHEET_TOKEN, body=payload)
        return credentials
