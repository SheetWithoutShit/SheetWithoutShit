"""Module that includes functionality to work with user`s data."""

import logging
from datetime import datetime

from asyncpg import exceptions


LOG = logging.getLogger(__name__)

GET_NOTIFICATIONS_ENABLED = """
    SELECT notifications_enabled
      FROM "USER"
     WHERE telegram_id=$1
"""
TRANSACTION_NOTIFICATION_TEXT = \
    "Транзакція! 💲\n\n" \
    "▪️ Сума: *{amount}*\n" \
    "▪️ Категорія: *{category}*\n" \
    "▪️ Додатково: *{info}*\n" \
    "▪️ Баланс: *{balance}*\n" \
    "▪ Дата: *{date}*"


class User:
    """Model that provides methods to work with user`s data."""

    def __init__(self, postgres=None, redis=None, bot=None):
        """Initialize user instance with required clients."""
        self._postgres = postgres
        self._redis = redis
        self._bot = bot

    async def is_notifications_enabled(self, user_id):
        """Return True if user enabled notifications, otherwise False."""
        try:
            record = await self._postgres.fetchone(GET_NOTIFICATIONS_ENABLED, user_id)
            return record["notifications_enabled"]
        except exceptions.PostgresError as err:
            LOG.error("Couldn't retrieve notifications for user=%s. Error: %s", user_id, err)
        except TypeError:
            LOG.error("User=%s doesn't not exist.", user_id)

    async def notify_user(self, user_id, transaction):
        """Notify user about accomplishment transaction."""
        if not await self.is_notifications_enabled(user_id):
            return

        mcc_codes = await self._redis.get("mcc", deserialize=True, default=[])
        category = mcc_codes.get(transaction["mcc"], "-")
        date = datetime.fromtimestamp(transaction["timestamp"]).strftime("%d.%m.%Y %H:%M:%S")
        text = TRANSACTION_NOTIFICATION_TEXT.format(
            amount=transaction["amount"],
            category=category,
            info=transaction["info"],
            balance=transaction["balance"],
            date=date
        )
        report_task = {
            "name": "send_message",
            "kwargs": {
                "user_id": user_id,
                "text": text,
                "parse_mode": "markdown",
                "disable_notification": False
            }
        }
        await self._redis.publish("task", report_task)
