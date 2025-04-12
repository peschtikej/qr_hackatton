from telebot.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
import logging

from bot import bot
from bot.models import User

logger = logging.getLogger(__name__)

def get_role_selection_markup() -> InlineKeyboardMarkup:
    """Create role selection markup"""
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("Учитель 👨‍🏫", callback_data="role_teacher"),
        InlineKeyboardButton("Родитель 👨‍👦", callback_data="role_parent")
    )
    return markup

def send_role_selection(user_id: int, username: str) -> None:
    """Send role selection buttons to user"""
    markup = get_role_selection_markup()
    bot.send_message(
        user_id,
        f"Здравствуйте, {username}! Пожалуйста, выберите вашу роль:",
        reply_markup=markup
    )

def send_role_confirmation(call: CallbackQuery, role: str) -> None:
    """Send confirmation buttons for selected role"""
    role_display = "Учитель" if role == "teacher" else "Родитель"
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("Да ✅", callback_data=f"confirm_{role}"),
        InlineKeyboardButton("Нет ❌", callback_data="cancel_role")
    )
    
    bot.edit_message_text(
        f"Вы выбрали: {role_display}\nВсё верно?",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )

def handle_role_selection(call: CallbackQuery) -> None:
    """Handle role selection callback"""
    user_id = call.from_user.id
    logger.info(f"Received callback with data: {call.data} from user {user_id}")
    
    try:
        if call.data.startswith("role_"):
            role = call.data.split("_")[1]  # Will be 'teacher' or 'parent'
            logger.info(f"User {user_id} selected role: {role}")
            send_role_confirmation(call, role)
        
        elif call.data.startswith("confirm_"):
            role = call.data.split("_")[1]  # Will be 'teacher' or 'parent'
            logger.info(f"User {user_id} confirming role: {role}")
            
            if role not in ['teacher', 'parent']:
                logger.error(f"Invalid role received: {role}")
                bot.answer_callback_query(call.id, "Неверная роль. Попробуйте еще раз.")
                return
                
            # Check if user already exists
            existing_user = User.objects.filter(user_id=user_id).first()
            if existing_user:
                logger.info(f"User {user_id} already exists with role {existing_user.role}")
                bot.answer_callback_query(call.id, "Вы уже зарегистрированы")
                return
                
            user = User.objects.create(
                user_id=user_id,
                role=role
            )
            logger.info(f"Created new user: {user}")
            
            role_display = "Учитель" if role == "teacher" else "Родитель"
            bot.edit_message_text(
                f"Отлично! Вы зарегистрированы как {role_display} ✅",
                call.message.chat.id,
                call.message.message_id
            )
            bot.answer_callback_query(call.id, "Регистрация успешно завершена!")
        
        elif call.data == "cancel_role":
            logger.info(f"User {user_id} cancelled role selection")
            bot.edit_message_text(
                "Пожалуйста, выберите вашу роль:",
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_role_selection_markup()
            )
            bot.answer_callback_query(call.id, "Выберите роль заново")
            
    except Exception as e:
        logger.error(f"Error in handle_role_selection: {str(e)}", exc_info=True)
        bot.send_message(call.message.chat.id, f"Произошла ошибка: {str(e)}")
        bot.answer_callback_query(call.id, "Произошла ошибка при обработке запроса") 