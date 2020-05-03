"""This module provides tasks related to user."""

import logging

__all__ = ["hello"]

LOG = logging.getLogger(__name__)


async def hello(uno, dunno):
    """Test task."""
    LOG.info("%s - %s", uno, dunno)
