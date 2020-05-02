"""This module provides API interactions with server side."""

import json
import requests


class API:
    """Class that provides http requests to server API."""

    def __init__(self, domain, bot_token):
        """Initialize API instance for further work with server API."""
        session = requests.Session()
        session.headers.update({"Authorization": bot_token})
        self.session = session
        self.domain = f"http://{domain}"

    def register_user(self, user):
        """Send request in order to create a new user."""
        endpoint = f"{self.domain}/user"
        user_json = json.dumps(user)
        response = self.session.post(endpoint, data=user_json)

        return response.json()

    def get_spreadsheet_auth_url(self):
        """Get request in order to retrieve spreadsheet auth url."""
        endpoint = f"{self.domain}/spreadsheet"
        response = self.session.get(endpoint)

        return response.json()

    def register_spreadsheet(self, telegram_id, auth_code):
        """Get request in order to retrieve spreadsheet auth url."""
        endpoint = f"{self.domain}/spreadsheet"
        data = json.dumps({"telegram_id": telegram_id, "auth_code": auth_code})
        response = self.session.post(endpoint, data=data)

        return response.json()
