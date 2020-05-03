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
        "first_name": request.from_user.first_name,
        "last_name": request.from_user.last_name
    }
    response = bot.api.register_user(request.chat.id, user)
    if not response.get("success"):
        bot.send_message(request.chat.id, text=messages.OOPS)
        return

    bot.send_message(request.chat.id, messages.START_TEXT)


@bot.message_handler(commands=["me"])
def handle_me_command(request):
    """Send all information about user."""
    response = bot.api.get_user(request.chat.id)
    if not response.get("success"):
        bot.send_message(request.chat.id, text=messages.OOPS)
        return

    user = response["user"]
    first_name = user["first_name"] or "Невідомець"
    last_name = user["last_name"] or ""
    spreadsheet = messages.CHECK_MARK if user["spreadsheet_refresh_token"] else messages.CROSS_MARK
    monobank = messages.CHECK_MARK if user["monobank_token"] else messages.CROSS_MARK

    text = messages.USER_INFO.format(
        first_name=first_name,
        last_name=last_name,
        spreadsheet=spreadsheet,
        monobank=monobank
    )
    bot.send_message(request.chat.id, text=text)


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


@bot.message_handler(commands=["monobank"])
def handle_monobank_command(request):
    """Send steps to get access to user`s monobank account."""
    message = bot.send_message(
        request.chat.id,
        text=messages.MONOBANK_AUTH,
        parse_mode="markdown"
    )
    bot.register_next_step_handler(message, handle_monobank_registration)


def handle_monobank_registration(request):
    """Handle step for activating user`s monobank account."""
    token = request.text.strip()
    response = bot.api.register_monobank(request.chat.id, token)
    if not response.get("success"):
        bot.send_message(request.chat.id, text=messages.OOPS)
        return

    bot.send_message(request.chat.id, text=messages.MONOBANK_AUTH_SUCCESS)
