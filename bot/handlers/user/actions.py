from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import logging

from bot import bot
from bot.models import User
from bot.handlers.common import get_parent_markup, get_teacher_markup

logger = logging.getLogger(__name__)

def get_back_markup() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("◀️ Назад", callback_data="back_to_menu")
    )
    return markup

def handle_back_to_menu(call: CallbackQuery) -> None:
    """Handle back button press"""
    try:
        user = User.objects.get(user_id=call.from_user.id)
        markup = get_parent_markup() if user.role == "parent" else get_teacher_markup()
        
        bot.edit_message_text(
            "Здравствуйте. Пожалуйста выберете действие 👇",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )
        bot.answer_callback_query(call.id)
    except User.DoesNotExist:
        bot.answer_callback_query(call.id, "Ошибка: пользователь не найден")

def handle_parent_actions(call: CallbackQuery) -> None:
    """Handle parent action buttons"""
    if call.data == "parent_mark_absent":
        bot.answer_callback_query(call.id)
        bot.edit_message_text(
            "Эта функция будет доступна в ближайшее время",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_back_markup()
        )

def handle_teacher_actions(call: CallbackQuery) -> None:
    """Handle teacher action buttons"""
    bot.answer_callback_query(call.id)
    
    if call.data == "teacher_mark_attendance":
        bot.edit_message_text(
            "Эта функция будет доступна в ближайшее время",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_back_markup()
        )
    elif call.data == "teacher_check_homework":
        bot.edit_message_text(
            "Эта функция будет доступна в ближайшее время",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_back_markup()
        )
    elif call.data == "teacher_check_present":
        from bot.handlers.user.qr_rec import start_qr_scanning
        # Convert callback query to message for start_qr_scanning
        message = call.message
        message.from_user = call.from_user
        start_qr_scanning(message) 