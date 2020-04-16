"""This module provides interactions with google spreadsheet API."""

from core.http import HTTPRequest

from endpoints import SPREADSHEET_API


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

    async def create_spreadsheet(self, token, spreadsheet_name):
        """Create a spreadsheet, return the newly created spreadsheet."""
        body = {"properties": {"title": spreadsheet_name}}
        headers = SpreadsheetAPI.format_headers(token)

        response = await self.post(url=SPREADSHEET_API, headers=headers, body=body)
        return response

    async def add_sheet(self, token, spreadsheet_id, sheet_name):
        """Add a new sheet to an existing user`s spreadsheet with provided name."""
        url = f"{SPREADSHEET_API}/{spreadsheet_id}:batchUpdate"
        body = {"requests": [{"addSheet": {"properties": {"title": sheet_name}}}]}
        headers = SpreadsheetAPI.format_headers(token)

        response = await self.post(url, headers=headers, body=body)
        return response

    async def get_sheet(self, token, spreadsheet_id, sheet_range):
        """
        Returns a range of values from a spreadsheet.
        In order to specify the values range use A1 notation.
        """
        url = f"{SPREADSHEET_API}/{spreadsheet_id}/values/{sheet_range}"
        headers = SpreadsheetAPI.format_headers(token)

        response = await self.get(url, headers=headers)
        return response

    async def update_sheet(self, token, spreadsheet_id, modifications, input_option):
        """Set values in one or more ranges of a spreadsheet."""
        url = f'{SPREADSHEET_API}/{spreadsheet_id}/values:batchUpdate'
        body = {"data": modifications, "valueInputOption": input_option}
        headers = SpreadsheetAPI.format_headers(token)

        response = await self.post(url, headers, body)
        return response
