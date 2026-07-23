import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database.db import init_db

# Barcha routerlarni chaqiramiz
from handlers import start, tap, admin, withdraw, ads
from middlewares.maintenance import MaintenanceMiddleware
from middlewares.check_admin import AdminMiddleware

async def main():
    logging.basicConfig(level=logging.INFO)
    
    await init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # 1. Global Middleware'larni ulash (Barcha xabarlar shu yerdan o'tadi)
    dp.message.middleware(MaintenanceMiddleware())

    # 2. Routerlarni ulash
    dp.include_router(start.router)
    dp.include_router(tap.router)
    dp.include_router(withdraw.router)
    dp.include_router(ads.router)
    
    # 3. Admin routeriga maxsus AdminMiddleware ni ulaymiz
    admin.router.message.middleware(AdminMiddleware())
    dp.include_router(admin.router)

    logging.info("Bot to'liq ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi.")
