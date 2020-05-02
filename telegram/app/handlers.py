"""This module provides main bot`s message handlers."""

from bot import Bot

import messages


bot = Bot()


@bot.message_handler(commands=["help"])
def handle_help_command(request):
    """Send help information to user."""
    bot.send_message(request.from_user.id, messages.HELP_TEXT)


@bot.message_handler(commands=["start"])
def handle_start_command(request):
    """Send start steps to user."""
    user = {
        "telegram_id": request.chat.id,
        "first_name": request.from_user.first_name,
        "last_name": request.from_user.last_name
    }
    bot.api.register_user(user)
    bot.send_message(request.chat.id, messages.START_TEXT)


@bot.message_handler(commands=["spreadsheet"])
def handle_spreadsheet_command(request):
    """Send steps to get access to user`s spreadsheet account."""
    response = bot.api.get_spreadsheet_auth_url()
    auth_url = response.get("auth_url")

    text = messages.SPREADSHEET_AUTH.format(auth_url=auth_url)
    message = bot.send_message(request.chat.id, text=text, parse_mode="markdown")

    bot.register_next_step_handler(message, handle_spreadsheet_registration)


def handle_spreadsheet_registration(request):
    """Handle step for activating user`s spreadsheet account."""
    auth_code = request.text.strip()
    response = bot.api.register_spreadsheet(request.chat.id, auth_code)
    if not response.get("success"):
        bot.send_message(request.chat.id, text=messages.OOPS)
        return

    bot.send_message(request.chat.id, text=messages.SPREADSHEET_AUTH_SUCCESS)
