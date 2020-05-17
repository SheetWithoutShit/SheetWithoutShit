"""This module provides API interactions with server side."""

import json
import requests


def parse_response(func):
    """Parse receive response to json format."""
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        try:
            return response.json()
        except json.JSONDecodeError:
            return {
                "success": False
            }

    return wrapper


class API:
    """Class that provides http requests to server API."""

    def __init__(self, domain, bot_token):
        """Initialize API instance for further work with server API."""
        session = requests.Session()
        session.headers.update({"Authorization": bot_token})
        self.session = session
        self.domain = f"http://{domain}"

    @parse_response
    def register_user(self, telegram_id, user):
        """Send request in order to create a new user."""
        endpoint = f"{self.domain}/user/{telegram_id}"
        user_json = json.dumps(user)
        response = self.session.post(endpoint, data=user_json)

        return response

    @parse_response
    def get_user(self, telegram_id):
        """Get request in order to retrieve user information."""
        endpoint = f"{self.domain}/user/{telegram_id}"
        response = self.session.get(endpoint)

        return response

    @parse_response
    def update_user(self, telegram_id, data):
        """Put request in order to update user information."""
        endpoint = f"{self.domain}/user/{telegram_id}"
        user_data = json.dumps(data)
        response = self.session.put(endpoint, data=user_data)

        return response

    @parse_response
    def get_spreadsheet_auth_url(self):
        """Get request in order to retrieve spreadsheet auth url."""
        endpoint = f"{self.domain}/spreadsheet"
        response = self.session.get(endpoint)

        return response

    @parse_response
    def register_spreadsheet(self, telegram_id, auth_code):
        """Send auth_code in order to get user`s spreadsheet credentials."""
        endpoint = f"{self.domain}/spreadsheet"
        data = json.dumps({"telegram_id": telegram_id, "auth_code": auth_code})
        response = self.session.post(endpoint, data=data)

        return response

    @parse_response
    def register_monobank(self, telegram_id, token):
        """Send token in order to get access to user`s monobank account."""
        endpoint = f"{self.domain}/monobank"
        data = json.dumps({"telegram_id": telegram_id, "token": token})
        response = self.session.post(endpoint, data=data)

        return response

    @parse_response
    def update_budget(self, telegram_id, data):
        """Put request in order to update user`s budget."""
        endpoint = f"{self.domain}/user/{telegram_id}/budget"
        budget_data = json.dumps(data)
        response = self.session.put(endpoint, data=budget_data)

        return response
