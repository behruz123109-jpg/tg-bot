import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, CommandObject
from aiogram.enums import ParseMode

# database.py dan funksiyalarni chaqirib olamiz
from database import init_db, add_user, get_setting

# O'zingizning bot tokeningizni shu yerga qo'yasiz (BotFather'dan olingan)
BOT_TOKEN = "8300434192:AAHQ-RvE9I0SsD_i61LEG5a1lZTScGhc8oM"

# Bot va Dispatcher yaratish
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: types.Message, command: CommandObject):
    user = message.from_user
    
    # 1. Texnik tanaffus (Maintenance) holatini tekshiramiz
    maintenance_mode = await get_setting('maintenance_mode')
    
    # Agar admin panelda tanaffus 1 qilingan bo'lsa, bot oddiy foydalanuvchilarga ishlamaydi
    # (Lekin sizni, ya'ni adminni tekshirib o'tkazib yuboradigan filtrni admin qismida qo'shamiz)
    if maintenance_mode == '1':
        await message.answer("🛠 <b>Botda profilaktika ishlari ketmoqda!</b>\nYangilanishlar yuklanmoqda. Tez orada qaytamiz, biroz kuting.")
        return

    # 2. Referal tizimi (Deep link orqali kim chaqirganini aniqlash)
    # Masalan: t.me/Botingiz_bot?start=123456789
    referrer_id = None
    if command.args and command.args.isdigit():
        referrer_id = int(command.args)
        if referrer_id == user.id:
            referrer_id = None # O'ziga o'zi referal bo'la olmaydi (Anti-cheat)

    # 3. Foydalanuvchini bazaga qo'shish
    # (database.py dagi INSERT OR IGNORE sababli, agar oldin kirgan bo'lsa xato bermaydi)
    await add_user(
        telegram_id=user.id,
        username=user.username,
        full_name=user.full_name,
        referrer_id=referrer_id
    )

    # 4. Bazadan start matnini o'qib olish (Admin Panelda o'zgartiriladigan matn)
    start_text = await get_setting('start_text')
    
    # Hoziroq vaqtincha oddiy xabar yuboramiz. 
    # Keyingi qadamda bunga chiroyli WebApp tugmasini qo'shamiz!
    await message.answer(f"Salom, <b>{user.full_name}</b>!\n\n{start_text}")

async def main():
    # Bot eshitishni boshlashidan oldin bazani yuklaymiz (Jadvallar yaratiladi)
    await init_db()
    logging.info("✅ Bot muvaffaqiyatli ishga tushdi!")
    
    # Bot yopiq paytida kelgan eskirgan xabarlarni o'tkazib yuborish (flood'ni oldini oladi)
    await bot.delete_webhook(drop_pending_updates=True) 
    
    # Botni polling rejimida ishga tushirish
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Loglarni ekranga chiqarish uchun
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
