"""This module provides main bot`s message handlers."""

import messages
from bot import Bot


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
    first_name = user["first_name"] or "Незнайомець"
    last_name = user["last_name"] or ""

    spreadsheet_id = user["spreadsheet"]
    notifications_mark = messages.CHECK_MARK if user["notifications_enabled"] else messages.CROSS_MARK
    spreadsheet_mark = messages.CHECK_MARK if spreadsheet_id else messages.CROSS_MARK

    spreadsheet_token_mark = messages.CHECK_MARK if user["spreadsheet_refresh_token"] else messages.CROSS_MARK
    monobank_mark = messages.CHECK_MARK if user["monobank_token"] else messages.CROSS_MARK

    text = messages.USER_INFO.format(
        first_name=first_name,
        last_name=last_name,
        notifications_mark=notifications_mark,
        spreadsheet_mark=spreadsheet_mark,
        spreadsheet_id=spreadsheet_id,
        monobank_mark=monobank_mark,
        spreadsheet_token_mark=spreadsheet_token_mark,
    )
    bot.send_message(request.chat.id, text=text, parse_mode="markdown")


@bot.message_handler(commands=["spreadsheet"])
def handle_spreadsheet_command(request):
    """Send steps to get access to user`s spreadsheet account."""
    response = bot.api.get_spreadsheet_auth_url()
    if not response.get("success"):
        bot.send_message(request.chat.id, text=messages.OOPS)
        return

    auth_url = response["auth_url"]
    text = messages.SPREADSHEET_AUTH.format(auth_url=auth_url)
    message = bot.send_message(request.chat.id, text=text, parse_mode="markdown")

    bot.register_next_step_handler(message, handle_spreadsheet_registration)


@bot.check_command
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


@bot.check_command
def handle_monobank_registration(request):
    """Handle step for activating user`s monobank account."""
    token = request.text.strip()
    response = bot.api.register_monobank(request.chat.id, token)
    if not response.get("success"):
        bot.send_message(request.chat.id, text=messages.OOPS)
        return

    bot.send_message(request.chat.id, text=messages.MONOBANK_AUTH_SUCCESS)


@bot.message_handler(commands=["savings"])
def handle_savings_command(request):
    """Send step in order to modify budget savings."""
    response = bot.api.get_user(request.chat.id)
    if not response.get("success"):
        bot.send_message(request.chat.id, text=messages.OOPS)
        return

    savings = response["user"]["savings"]
    text = messages.SAVINGS_ACTION.format(savings=savings)
    message = bot.send_message(request.chat.id, text=text)
    bot.register_next_step_handler(message, handle_savings_modification)


@bot.check_command
def handle_savings_modification(request):
    """Handle step to modify user`s savings by provided integer."""
    if not request.text.strip().isdigit():
        bot.send_message(request.chat.id, text=messages.OOPS)
        return

    response = bot.api.update_savings(request.chat.id, int(request.text))
    if not response.get("success"):
        bot.send_message(request.chat.id, text=messages.OOPS)
        return

    bot.send_message(request.chat.id, text=messages.SAVINGS_SUCCESS)


@bot.message_handler(commands=["notifications_on", "notifications_off"])
def handle_notifications_on_command(request):
    """Handle notification action command in order to (de)activate notifications.."""
    notifications_enabled = request.text.startswith("/notifications_on")
    user_data = {"notifications_enabled": notifications_enabled}
    response = bot.api.update_user(request.chat.id, user_data)
    if not response.get("success"):
        bot.send_message(request.chat.id, text=messages.OOPS)
        return

    notifications_action = "активовано" if notifications_enabled else "деактивовано"
    text = messages.NOTIFICATION_ACTIONS.format(action=notifications_action)
    bot.send_message(request.chat.id, text=text)


@bot.message_handler(content_types=['text'])
def handle_atypical_command(request):
    """Send available commands to user."""
    commands = "\n▪ ".join(bot.commands)
    text = messages.INVALID_TEXT.format(commands=commands)
    bot.send_message(request.from_user.id, text)
