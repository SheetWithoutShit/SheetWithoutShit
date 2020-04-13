"""This module provides functionality for async http interactions."""

import aiohttp


class HTTPRequest:
    """Class that provides http basic async requests."""

    def __init__(self):
        """Initialize client session for async http requests."""
        self.session = aiohttp.ClientSession()

    async def get(self, url, headers=None, params=None):
        """Return response from async get http request in json format."""
        async with self.session.get(url, headers=headers, params=params) as response:
            return await response.json()

    async def post(self, url, headers=None, body=None):
        """Return response from async post http request in json format."""
        async with self.session.post(url, headers=headers, json=body) as response:
            return await response.json()

    async def delete(self, url, headers=None):
        """Return response from async delete http request in json format."""
        async with self.session.delete(url, headers=headers) as response:
            return await response.json()

    async def put(self, url, headers=None, body=None):
        """Return response from async put http request in json format."""
        async with self.session.delete(url, headers=headers, json=body) as response:
            return await response.json()
