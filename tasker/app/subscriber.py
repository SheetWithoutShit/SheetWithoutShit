"""This module provides functionality for Redis subscribing."""

import os
import json
import logging

import aioredis


LOG = logging.getLogger(__name__)


class TaskReader:
    """Class that provides subscriber`s functionality."""

    stop_task = "STOP ME!"
    ping_task = "PING!"

    def __init__(self):
        """Initialize redis connection instance with env configs."""
        self.pid = None
        self.redis = None
        self.channel = None
        self.channel_name = None

        host = os.environ["REDIS_HOST"]
        port = os.environ["REDIS_PORT"]
        self.address = (host, port)
        self.password = os.environ.get("REDIS_PASSWORD")

    @classmethod
    async def create(cls, pid):
        """Create high-level interface instance bound to single connection."""
        instance = cls()
        instance.pid = pid
        instance.redis = await aioredis.create_redis(
            address=instance.address,
            password=instance.password,
        )

        return instance

    @staticmethod
    def parse_task_info(message):
        """Return parsed information about task."""
        task = json.loads(message)
        return task["name"], task.get("kwargs", {})

    async def subscribe(self, channel_name):
        """Subscribe to provided channel."""
        self.channel, *_ = await self.redis.subscribe(channel_name)
        self.channel_name = self.channel.name.decode("utf-8")

    async def close(self):
        """Unsubscribe from channel and close redis connection."""
        await self.redis.unsubscribe(self.channel_name)

        self.redis.close()
        await self.redis.wait_closed()

    async def read(self, scheduler):
        """Infinity reading messages from redis broker and spawning tasks."""
        LOG.debug("%s. Start reading tasks from channel: <%s>", self.pid, self.channel_name)

        while await self.channel.wait_message():
            message = await self.channel.get(encoding="utf-8")

            try:
                task, kwargs = TaskReader.parse_task_info(message)
            except (json.JSONDecodeError, KeyError) as err:
                LOG.error("%s. Received invalid task: %s. Error: ", self.pid, err)
                continue

            if task == self.ping_task:
                LOG.info("%s. Someone annoying me with the message: %s", self.pid, message)
                continue
            if task == self.stop_task:
                LOG.info("%s. Received stop task. Starting self-destruction.", self.pid)
                return

            LOG.info("%s. Received task: %s", self.pid, message)
            await scheduler.spawn(task, kwargs)
