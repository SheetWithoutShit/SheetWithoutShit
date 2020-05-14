"""This module provides functionality for Redis subscribing."""

import json
import logging

import aioredis

from core.database.redis import PoolManager as Redis


LOG = logging.getLogger(__name__)


class TaskReader:
    """Class that provides subscriber`s functionality."""

    stop_task = "STOP ME!"
    ping_task = "PING!"

    def __init__(self):
        """Initialize redis connection instance with env configs."""
        self.redis_conn = None
        self.channel = None
        self.channel_name = "task"

    @classmethod
    async def create(cls):
        """Create high-level interface instance bound to single connection."""
        instance = cls()
        instance.redis_conn = await Redis.create_connection()

        return instance

    async def subscribe(self):
        """Subscribe to provided channel."""
        self.channel = aioredis.Channel(name=self.channel_name, is_pattern=False)
        await self.redis_conn.execute_pubsub("subscribe", self.channel)

    async def close(self):
        """Unsubscribe from channel and close redis connection."""
        await self.redis_conn.execute_pubsub("unsubscribe", self.channel_name)
        self.channel.close()

        self.redis_conn.close()
        await self.redis_conn.wait_closed()

    async def read(self, scheduler):
        """Infinity reading messages from redis broker and spawning tasks."""
        LOG.debug("Start reading tasks from channel: <%s>", self.channel_name)

        while await self.channel.wait_message():
            message = await self.channel.get(encoding="utf-8", decoder=json.loads)

            try:
                task, kwargs = message["name"], message.get("kwargs", {})
            except KeyError as err:
                LOG.error("Received invalid task: %s. Error: ", err)
                continue

            if task == self.ping_task:
                LOG.info("Someone annoying me with the message: %s", message)
                continue
            if task == self.stop_task:
                LOG.info("Received stop task. Starting self-destruction.")
                return

            LOG.info("Received task: %s", message)
            await scheduler.spawn(task, kwargs)
