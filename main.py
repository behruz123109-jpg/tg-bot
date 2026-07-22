import asyncio
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import database

BOT_TOKEN = "SIZNING_BOT_TOKENINGIZ"
ADMIN_ID = 123456789 # Telegram ID raqamingiz
WEBAPP_URL = "https://sizning-saytingiz.uz/index.html"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

class AdminStates(StatesGroup):
    waiting_for_card = State()
    waiting_for_price = State()
    waiting_for_task_title = State()

@dp.message(CommandStart())
async def start(message: types.Message):
    database.add_user(message.from_user.id, message.from_user.username)
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 O'yinga kirish", web_app=WebAppInfo(url=WEBAPP_URL))]
    ])
    await message.answer(f"Salom {message.from_user.first_name}! O'yinga xush kelibsiz.", reply_markup=markup)

# ================= ADMIN PANEL =================
@dp.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    
    card = database.get_setting("admin_card")
    price = database.get_setting("olmos_price")
    
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"💳 Kartani o'zgartirish ({card})", callback_data="change_card")],
        [InlineKeyboardButton(text=f"💵 Olmos narxi ({price} so'm)", callback_data="change_price")],
        [InlineKeyboardButton(text="➕ Yangi vazifa qo'shish", callback_data="add_task")]
    ])
    await message.answer("👑 **Admin Boshqaruv Paneli:**\nNimani o'zgartirmoqchisiz?", reply_markup=markup, parse_mode="Markdown")

@dp.callback_query(F.data == "change_card")
async def edit_card_start(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Yangi Karta raqami va Egalari ismini yozing:\n*Masalan: 8600123456789012 (Behruz A.)*", parse_mode="Markdown")
    await state.set_state(AdminStates.waiting_for_card)

@dp.message(AdminStates.waiting_for_card)
async def edit_card_save(message: types.Message, state: FSMContext):
    database.set_setting("admin_card", message.text)
    await message.answer("✅ Karta raqami muvaffaqiyatli o'zgartirildi!")
    await state.clear()

@dp.callback_query(F.data == "change_price")
async def edit_price_start(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("1 ta Olmosning narxini so'mda kiriting:\n*Masalan: 120*", parse_mode="Markdown")
    await state.set_state(AdminStates.waiting_for_price)

@dp.message(AdminStates.waiting_for_price)
async def edit_price_save(message: types.Message, state: FSMContext):
    database.set_setting("olmos_price", message.text)
    await message.answer("✅ Olmos narxi o'zgartirildi!")
    await state.clear()

# WebApp dan kelgan so'rovlar (Sotib olish / Yechish)
@dp.message(F.web_app_data)
async def web_app_handler(message: types.Message):
    data = json.loads(message.web_app_data.data)
    
    if data['action'] == 'buy_real':
        card = database.get_setting("admin_card")
        price = data['price']
        amount = data['amount']
        
        msg = (
            f"💎 **{amount} Olmos** sotib olish so'rovi.\n\n"
            f"💵 To'lov summasi: **{price} so'm**\n"
            f"💳 Karta: `{card}`\n\n"
            f"To'lovni bajaring va chek (skrinshot) yuboring!"
        )
        await message.answer(msg, parse_mode="Markdown")

async def main():
    database.init_db()
    print("🤖 Bot va Admin Panel tayyor!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
