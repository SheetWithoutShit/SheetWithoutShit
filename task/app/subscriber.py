"""This module provides functionality for Redis subscribing."""

import os
import logging

import aioredis


LOG = logging.getLogger(__name__)


class RedisSubscriber:
    """Class that provides subscriber`s functionality."""

    stop_word = "STOP ME!"

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
        while await self.channel.wait_message():
            task = await self.channel.get(encoding="utf-8")
            LOG.info("%s. Channel: <%s>. Task: %s", self.pid, self.channel_name, task)

            if task == self.stop_word:
                return

            await scheduler.spawn(task)
