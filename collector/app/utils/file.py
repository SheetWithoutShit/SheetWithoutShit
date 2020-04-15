"""This module provides interactions with files."""

import json

from aiofiles import open as async_open


async def write_json(data, file_name):
    """Async function for writing json file."""
    async with async_open(f"{file_name}.json", 'w') as file:
        await file.write(json.dumps(data))
