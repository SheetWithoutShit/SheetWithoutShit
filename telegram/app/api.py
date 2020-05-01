"""This module provides API interactions with server side."""

import json
import requests


class API:
    """Class that provides http requests to server API."""

    def __init__(self, domain, bot_token):
        """Initialize API instance for further work with server API."""
        session = requests.Session()
        session.headers.update({"Auth": bot_token})
        self.session = session
        self.domain = f"http://{domain}"

    def register_user(self, telegram_id):
        """Send request in order to create a new user."""
        endpoint = f"{self.domain}/user"
        data = json.dumps({"telegram_id": telegram_id})
        response = self.session.post(endpoint, data=data)

        return response
