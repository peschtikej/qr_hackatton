from telebot.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from typing import Dict, List
import logging

from bot import bot
from bot.api.qr_scanner import scan_qr_code
from bot.handlers.user.actions import get_back_markup

logger = logging.getLogger(__name__)

# Store scanning states for users
scanning_states: Dict[int, bool] = {}

def parse_student_data(qr_data: str) -> tuple:
    """Parse student data from QR code"""
    try:
        parts = qr_data.split('.')
        if len(parts) < 7:
            return None
            
        surname = parts[0]
        name = parts[1]
        patronymic = parts[2]
        teacher_name = parts[-2]
        class_info = parts[-3]
        
        return (f"{surname} {name} {patronymic}", class_info, teacher_name)
    except Exception as e:
        logger.error(f"Error parsing student data: {e}")
        return None

def start_qr_scanning(message: Message) -> None:
    """Start QR code scanning mode"""
    user_id = message.from_user.id
    scanning_states[user_id] = True
    
    markup = get_back_markup()
    bot.send_message(
        user_id,
        "Отправляйте фотографии QR кодов учеников.\n"
        "Нажмите ◀️ Назад, когда закончите сканирование.",
        reply_markup=markup
    )

def handle_qr_photo(message: Message) -> None:
    """Handle received QR code photo"""
    user_id = message.from_user.id
    
    # Check if user is in scanning mode
    if not scanning_states.get(user_id):
        return
        
    try:
        # Get the highest resolution photo
        photo = message.photo[-1]
        file_info = bot.get_file(photo.file_id)
        photo_data = bot.download_file(file_info.file_path)
        
        # Scan QR codes
        results = scan_qr_code(photo_data)
        markup = get_back_markup()
        
        if not results:
            bot.send_message(
                message.chat.id,
                "QR код не найден. Попробуйте другое фото.",
                reply_markup=markup
            )
            return
        
        # Collect all valid student data
        students_info: List[str] = []
        errors = []
            
        # Process each QR code found
        for result in results:
            qr_data = result['data']
            parsed_data = parse_student_data(qr_data)
            
            if parsed_data:
                full_name, class_info, teacher_name = parsed_data
                students_info.append(
                    f"👨‍🎓 *{full_name}* ({class_info})\n"
                    f"👨‍🏫 Классный руководитель: *{teacher_name}*"
                )
            else:
                errors.append("❌ Обнаружен QR код с неверным форматом данных")
        
        # Send combined message with all students
        if students_info:
            message_text = "Обнаружены ученики на уроке:\n\n" + "\n\n".join(students_info)
            if errors:
                message_text += "\n\n" + "\n".join(errors)
                
            bot.send_message(
                message.chat.id,
                message_text,
                parse_mode="Markdown",
                reply_markup=markup
            )
        else:
            bot.send_message(
                message.chat.id,
                "Ошибка: неверный формат QR кодов",
                reply_markup=markup
            )
                
    except Exception as e:
        logger.error(f"Error processing QR photo: {e}")
        markup = get_back_markup()
        bot.send_message(
            message.chat.id,
            "Произошла ошибка при обработке QR кода",
            reply_markup=markup
        )

def stop_qr_scanning(call: CallbackQuery) -> None:
    """Stop QR code scanning mode"""
    user_id = call.from_user.id
    if user_id in scanning_states:
        del scanning_states[user_id]
    
    from bot.handlers.user.actions import handle_back_to_menu
    handle_back_to_menu(call)