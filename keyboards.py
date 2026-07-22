from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

def get_main_menu(is_admin: bool = False):
    """Asosiy menyu klaviaturasi (Reply Keyboard)"""
    keyboard = [
        [
            # WebApp ochiladigan asosiy o'yin tugmasi
            KeyboardButton(text="🎮 O'ynash", web_app=WebAppInfo(url="https://sizning-webapp-domenurfingiz.uz"))
        ],
        [
            KeyboardButton(text="👤 Profil"),
            KeyboardButton(text="🏆 Reyting")
        ],
        [
            KeyboardButton(text="🎁 Kunlik Bonus"),
            KeyboardButton(text="👥 Referallar")
        ],
        [
            KeyboardButton(text="❓ Yordam / Qoidalar")
        ]
    ]
    
    # Agar foydalanuvchi Admin bo'lsa, avtomatik ravishda Admin Panel tugmasini ham qo'shamiz
    if is_admin:
        keyboard.append([KeyboardButton(text="👑 Admin Panel")])
        
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
