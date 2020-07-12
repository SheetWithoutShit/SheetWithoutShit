"""This module provides tasks related to interactions with monobank."""

import logging
from datetime import datetime

from asyncpg import exceptions


__all__ = ["send_message", "send_daily_report"]


LOG = logging.getLogger(__name__)


GET_BUDGET_INFO = """
    SELECT budget.savings, budget.income, spent_month_costs, spent_daily_costs
    FROM "BUDGET" as budget
    LEFT JOIN (
        SELECT user_id, ABS(sum(amount)) as spent_month_costs
        FROM "TRANSACTION"
        WHERE user_id=$1
            and amount >= 0
            and timestamp between DATE_TRUNC('month', CURRENT_TIMESTAMP) and DATE_TRUNC('day', CURRENT_TIMESTAMP)
        GROUP BY user_id
    ) as transct_month ON budget.user_id=transct_month.user_id
    LEFT JOIN (
        SELECT user_id, ABS(sum(amount)) as spent_daily_costs
        FROM "TRANSACTION"
        WHERE user_id=$1
            and amount >= 0
            and timestamp between DATE_TRUNC('day', CURRENT_TIMESTAMP) - INTERVAL '1 day' 
                and DATE_TRUNC('day', CURRENT_TIMESTAMP)
        GROUP BY user_id
    ) as transct_daily ON budget.user_id=transct_daily.user_id
    WHERE budget.user_id=$1
        and budget.year = EXTRACT(YEAR FROM CURRENT_TIMESTAMP)
        and budget.month = EXTRACT(MONTH FROM CURRENT_TIMESTAMP)
"""

DAILY_REPORT_TEXT = \
    "Щоденний звіт! 💲\n\n" \
    "Денний бюджет: *{budget}*\n" \
    "▪️ Витрачено: *{spent}*\n" \
    "▪️ Заощаджено: *{saved}*\n"


async def send_message(pools, user_id, text, parse_mode="markdown", disable_notification=False):
    """Send message to user telegram account with provided configurations."""
    bot = pools["bot"]
    await bot.send_message(
        chat_id=user_id,
        text=text,
        parse_mode=parse_mode,
        disable_notification=disable_notification
    )


async def send_daily_report(pools, user_id):
    """Send daily report to user telegram account."""
    postgres = pools["postgres"]
    try:
        record = await postgres.fetchone(GET_BUDGET_INFO, user_id)
    except exceptions.PostgresError as err:
        LOG.error("Couldn't select budget info for user: %s. Error: %s", user_id, err)
        return

    def days_count():
        """Return count of days by the end of current month."""
        today = datetime.today()
        delta = today.replace(month=today.month + 1, day=1) - today
        return delta.days or 1

    available_budget = record["income"] / 100 * (record["savings"] or 1) - record["spent_month_costs"]
    daily_budget = available_budget / days_count()

    text = DAILY_REPORT_TEXT.format(
        budget=daily_budget,
        spent=record["spent_daily_costs"],
        saved=daily_budget - record["spent_daily_costs"]
    )
    await send_message(pools, user_id, text, parse_mode="markdown", disable_notification=True)
