import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, CommandObject
from aiogram.enums import ParseMode

from database import init_db, add_user, get_setting
from keyboards import get_main_menu

BOT_TOKEN = "8300434192:AAHQ-RvE9I0SsD_i61LEG5a1lZTScGhc8oM"
# O'zingizning Telegram ID'ingizni shu yerga yozasiz (Admin bo'lish uchun)
ADMIN_IDS = [8488028783] 

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: types.Message, command: CommandObject):
    user = message.from_user
    
    # Texnik tanaffus (Maintenance) tekshiruvi
    maintenance_mode = await get_setting('maintenance_mode')
    if maintenance_mode == '1' and user.id not in ADMIN_IDS:
        await message.answer("🛠 <b>TapMasterBot profilaktika rejimida!</b>\nTez orada qaytamiz.")
        return

    # Referal ID ni aniqlash
    referrer_id = None
    if command.args and command.args.isdigit():
        referrer_id = int(command.args)
        if referrer_id == user.id:
            referrer_id = None

    # Bazaga qo'shish
    await add_user(
        telegram_id=user.id,
        username=user.username,
        full_name=user.full_name,
        referrer_id=referrer_id
    )

    start_text = await get_setting('start_text')
    
    # Foydalanuvchi adminmi yoki yo'qligini tekshiramiz
    is_admin = user.id in ADMIN_IDS
    
    # Matn va klaviaturani birga yuboramiz
    await message.answer(
        f"Salom, <b>{user.full_name}</b>! 🎮 <b>TapMasterBot</b>'ga xush kelibsiz.\n\n{start_text}",
        reply_markup=get_main_menu(is_admin)
    )

async def main():
    await init_db()
    logging.info("✅ TapMasterBot muvaffaqiyatli ishga tushdi!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
