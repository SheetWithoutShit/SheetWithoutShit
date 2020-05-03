"""This module provides functionality to spawn tasks."""

import logging
import asyncio

import aiojobs


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

        instance.scheduler = scheduler
        instance.tasks = tasks

        return instance

    async def spawn(self, task_name, kwargs):
        """Spawn task with provided args/kwargs if available."""
        task = getattr(self.tasks, task_name, None)
        if not task:
            LOG.error("Task <%s> is not registered", task_name)
            return

        await task(**kwargs)

    async def close(self):
        """
        Wait to finish all active, pending tasks
        and gracefully close scheduler loop.
        """
        active, pending = self.scheduler.active_count, self.scheduler.pending_count
        while active or pending:
            LOG.info("%s. Waiting to finish tasks: active=%s, pending=%s", self.pid, active, pending)
            await asyncio.sleep(DEFAULT_SLEEP_TIME)
            active, pending = self.scheduler.active_count, self.scheduler.pending_count

        await self.scheduler.close()
