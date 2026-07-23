from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def tap_keyboard(coins: int, energy: int):
    kb = [
        [InlineKeyboardButton(text=f"👆 TAP! ({coins} 🪙 | ⚡ {energy})", callback_data="do_tap")],
        [InlineKeyboardButton(text="🔄 Yangilash", callback_data="refresh_tap")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)
