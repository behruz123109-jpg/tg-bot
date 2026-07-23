from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    kb = [
        [KeyboardButton(text="⚡ Tap (Tanga yig'ish)"), KeyboardButton(text="💎 Balans va Hamyon")],
        [KeyboardButton(text="👥 Taklif qilish"), KeyboardButton(text="ℹ️ Yordam")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
