"""This module provides functionality to spawn tasks."""

import logging
import asyncio

import aiojobs

from core.http import HTTPRequest
from core.database.postgres import PoolManager as PGPoolManager
from core.database.redis import PoolManager as RedisPoolManager


LOG = logging.getLogger(__name__)
DEFAULT_SLEEP_TIME = 5


def _exception_handler(scheduler, context):
    """Log exception caused in task job."""
    job, error = context["job"], context["exception"]
    LOG.error(
        "%s. Task <%s> failed. Error: %s",
        scheduler.pid,
        job._coro.__name__,  # pylint: disable=protected-access
        error
    )


class TaskScheduler:
    """Class that provides functionally for spawning tasks."""

    def __init__(self):
        """Initialize task scheduler instance."""
        self.pid = None
        self.scheduler = None
        self.tasks = None
        self.pools = None

    @classmethod
    async def create(cls, pid, tasks, limit, pending_limit):
        """Create task scheduler instance."""
        instance = cls()
        scheduler = await aiojobs.create_scheduler(
            limit=limit,
            pending_limit=pending_limit,
            exception_handler=_exception_handler,
        )
        setattr(scheduler, "pid", pid)

        pools = {
            "postgres": await PGPoolManager.create(),
            "redis": await RedisPoolManager.create(),
            "http": HTTPRequest()
        }

        instance.scheduler = scheduler
        instance.tasks = tasks
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
        active, pending = self.scheduler.active_count, self.scheduler.pending_count
        while active or pending:
            LOG.debug("%s. Waiting to finish tasks: active=%s, pending=%s", self.pid, active, pending)
            await asyncio.sleep(DEFAULT_SLEEP_TIME)
            active, pending = self.scheduler.active_count, self.scheduler.pending_count

        await self.scheduler.close()
