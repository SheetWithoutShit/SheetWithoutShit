"""This module provides main bot`s message handlers."""

from bot import Bot

import messages


bot = Bot()


@bot.message_handler(commands=['help'])
def handle_help_command(message):
    """Send help information to user."""
    bot.send_message(message.from_user.id, messages.HELP_TEXT)


@bot.message_handler(commands=['start'])
def handle_start_command(message):
    """Send start steps to user."""
    bot.api.register_user(message.chat.id)
    bot.send_message(message.chat.id, messages.START_TEXT)
