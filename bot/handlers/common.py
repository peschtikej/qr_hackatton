from telebot.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)

from bot import bot
from bot.models import User
from bot.handlers.user.registration import send_role_selection

def get_parent_markup() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            "Отметить ученика что нет на уроке", 
            callback_data="parent_mark_absent"
        )
    )
    return markup

def get_teacher_markup() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("Отметить вход/выход", callback_data="teacher_mark_attendance")
    )
    markup.row(
        InlineKeyboardButton("Проверить домашнее задание", callback_data="teacher_check_homework")
    )
    markup.row(
        InlineKeyboardButton("Проверить учеников на уроке", callback_data="teacher_check_present")
    )
    return markup

def start(message: Message) -> None:
    user_id = message.from_user.id
    username = message.from_user.username or "there"
    
    try:
        user = User.objects.get(user_id=user_id)
        if user.role == "parent":
            markup = get_parent_markup()
        else:  # teacher
            markup = get_teacher_markup()
            
        bot.send_message(
            user_id,
            "Здравствуйте. Пожалуйста выберете действие 👇",
            reply_markup=markup
        )
    except User.DoesNotExist:
        send_role_selection(user_id, username)