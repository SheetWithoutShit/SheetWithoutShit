"""This module provides functionality to spawn tasks."""

import logging
import asyncio

import aiojobs

from core.http import HTTPRequest
from core.database.postgres import PoolManager as PGPoolManager
from core.database.redis import PoolManager as RedisPoolManager

import tasks


LOG = logging.getLogger(__name__)


def _exception_handler(scheduler, context):
    """Log exception caused in task job."""
    job, error = context["job"], context["exception"]
    LOG.error(
        "%s. Task <%s> failed. Error: %s",
        scheduler.__name__,
        job._coro.__name__,  # pylint: disable=protected-access
        error
    )


class TaskScheduler:
    """Class that provides functionally for spawning tasks."""

    def __init__(self):
        """Initialize task scheduler instance."""
        self.scheduler = None
        self.pools = None
        self.tasks = tasks

    @classmethod
    async def create(cls):
        """Create task scheduler instance."""
        instance = cls()
        scheduler = await aiojobs.create_scheduler(exception_handler=_exception_handler)

        pools = {
            "postgres": await PGPoolManager.create(),
            "redis": await RedisPoolManager.create(),
            "http": HTTPRequest()
        }

        instance.scheduler = scheduler
        instance.pools = pools

        return instance

    async def spawn(self, task_name, kwargs):
        """Spawn task with provided args/kwargs if available."""
        task = getattr(self.tasks, task_name, None)
        if not task:
            LOG.error("Task <%s> is not registered", task_name)
            return

        await task(self.pools, **kwargs)

    async def close(self):
        """
        Wait to finish all active, pending tasks
        and gracefully close scheduler loop.
        """
        wait_time = 5
        active, pending = self.scheduler.active_count, self.scheduler.pending_count
        while active or pending:
            LOG.debug("Waiting to finish tasks: active=%s, pending=%s", active, pending)
            await asyncio.sleep(wait_time)
            active, pending = self.scheduler.active_count, self.scheduler.pending_count

        for pool in [self.scheduler, *self.pools.values()]:
            await pool.close()
