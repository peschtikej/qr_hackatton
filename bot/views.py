from traceback import format_exc
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.conf import settings
from telebot.apihelper import ApiTelegramException
from telebot.types import Update
from asgiref.sync import sync_to_async

from bot import bot
from bot.handlers.common import start
from bot.handlers.user.qr_rec import handle_qr_photo, stop_qr_scanning
from bot.handlers.user.registration import handle_role_selection
from bot.handlers.user.actions import handle_parent_actions, handle_teacher_actions, handle_back_to_menu

@require_GET
def set_webhook(request: HttpRequest) -> JsonResponse:
    """Setting webhook."""
    bot.set_webhook(url=f"{settings.HOOK}/bot/{settings.BOT_TOKEN}")
    bot.send_message(settings.OWNER_ID, "webhook set")
    return JsonResponse({"message": "OK"}, status=200)


@require_GET
def status(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"message": "OK"}, status=200)


@csrf_exempt
@require_POST
@sync_to_async
def index(request: HttpRequest) -> JsonResponse:
    if request.META.get("CONTENT_TYPE") != "application/json":
        return JsonResponse({"message": "Bad Request"}, status=403)

    json_string = request.body.decode("utf-8")
    update = Update.de_json(json_string)
    try:
        bot.process_new_updates([update])
    except ApiTelegramException as e:
        bot.send_message(settings.GROUP_ID, f"Telegram exception. {e} {format_exc()}")
    except ConnectionError as e:
        bot.send_message(settings.GROUP_ID, f"Connection error. {e} {format_exc()}")
    except Exception as e:
        bot.send_message(settings.GROUP_ID, f"Unhandled exception. {e} {format_exc()}")
    return JsonResponse({"message": "OK"}, status=200)


"""
Common
"""

start = bot.message_handler(commands=["start"])(start)

# QR code handlers
qr_photo = bot.message_handler(content_types=["photo"])(handle_qr_photo)

# Registration handlers
role_selection = bot.callback_query_handler(
    func=lambda call: call.data.startswith(("role_", "confirm_", "cancel_role"))
)(handle_role_selection)

# Parent action handlers
parent_actions = bot.callback_query_handler(
    func=lambda call: call.data.startswith("parent_")
)(handle_parent_actions)

# Teacher action handlers
teacher_actions = bot.callback_query_handler(
    func=lambda call: call.data.startswith("teacher_")
)(handle_teacher_actions)

# Back button handler
back_button = bot.callback_query_handler(
    func=lambda call: call.data == "back_to_menu"
)(stop_qr_scanning)