import asyncio
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice, PreCheckoutQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import database

BOT_TOKEN = "8041760588:AAHA1eLxU46HPDIaL4o-k16eAjc-TUNKHzY" # Tokenni yozing
ADMIN_ID = 8488028783 # O'z ID raqamingizni yozing
WEBAPP_URL = "https://sizning-domeningiz.uz/index.html" # Hostingiz manzili

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

class AppState(StatesGroup):
    waiting_for_channel = State()
    waiting_for_broadcast = State()
    waiting_for_pubg_id = State()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    database.add_user(message.from_user.id, message.from_user.username)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 O'yinni boshlash", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton(text="📢 Homiylar kanallari", callback_data="check_channels")]
    ])
    await message.answer(
        f"Salom, {message.from_user.first_name}!\n\n👑 UC Miner Pro loyihasiga xush kelibsiz.\nTugmani bosing va 💎 UC-Chip ishlashni boshlang!",
        reply_markup=keyboard
    )

# ================= TELEGRAM STARS VA WEBAPP =================
@dp.message(F.web_app_data)
async def web_app_data_handler(message: types.Message, state: FSMContext):
    data = json.loads(message.web_app_data.data)
    
    if data['action'] == 'buy_stars':
        prices = [LabeledPrice(label="5,000 💎 UC-Chip", amount=100)] # 100 Stars
        await bot.send_invoice(
            chat_id=message.chat.id,
            title="💎 Olmos sotib olish",
            description="Hisobingizni to'ldiring va tezroq PUBG UC yechib oling!",
            payload="buy_5000_diamonds",
            provider_token="", # Stars uchun bo'sh bo'ladi
            currency="XTR",
            prices=prices
        )
    elif data['action'] == 'withdraw_uc':
        await message.answer("🎁 Yechib olish so'rovi boshlandi.\nIltimos, PUBG ID raqamingizni yuboring:")
        await state.set_state(AppState.waiting_for_pubg_id)

@dp.message(AppState.waiting_for_pubg_id)
async def process_pubg_id(message: types.Message, state: FSMContext):
    pubg_id = message.text
    # Bu yerda foydalanuvchi hisobidan 10000 chip yechib olish logikasi ulanadi
    database.add_withdrawal(message.from_user.id, 10000, pubg_id)
    await message.answer("✅ So'rovingiz adminlarga yuborildi. UC tez orada hisobingizga tushadi!")
    await state.clear()

@dp.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message(F.successful_payment)
async def successful_payment_handler(message: types.Message):
    if message.successful_payment.invoice_payload == "buy_5000_diamonds":
        database.add_chips(message.from_user.id, 5000)
        await message.answer("🎉 To'lov muvaffaqiyatli! Hisobingizga 5,000 💎 qo'shildi.")

# ================= ADMIN PANEL =================
@dp.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    total_users, pending_w = database.get_stats()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Statistika", callback_data="admin_stats")],
        [InlineKeyboardButton(text="📢 Kanallar", callback_data="admin_channels")],
        [InlineKeyboardButton(text=f"💳 Chiqim so'rovlari ({pending_w})", callback_data="admin_withdrawals")],
        [InlineKeyboardButton(text="✉️ Xabar yuborish", callback_data="admin_broadcast")]
    ])
    await message.answer("👑 **Admin Panel:**", reply_markup=keyboard, parse_mode="Markdown")

# [Admin panel logikalari oldingi kod bilan bir xil ishlaydi, joyni tejash uchun asosiy qismlar qoldirildi]

async def main():
    database.init_db()
    print("🚀 Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
