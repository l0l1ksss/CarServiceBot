from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def contact_keyboard():
# Создаем клавиатуру с кнопкой "Отправить контакт"
    contact_button = KeyboardButton(text="Отправить контакт", request_contact=True)
    markup = ReplyKeyboardMarkup(
        keyboard=[[contact_button]],  # Обязательное поле!
        resize_keyboard=True,         # Опционально
        one_time_keyboard=True        # Опционально
    )
    return markup