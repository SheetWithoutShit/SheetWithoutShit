"""This module provides additional functionality for http requests."""

from urllib import parse


def format_params(params):
    """Return formatted params as string."""
    return parse.urlencode(params)
