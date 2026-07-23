import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database.db import init_db
from handlers import start, tap

async def main():
    logging.basicConfig(level=logging.INFO)
    
    # DB ni tayyorlash
    await init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Routerlarni ulash
    dp.include_router(start.router)
    dp.include_router(tap.router)

    logging.info("Bot muvaffaqiyatli ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi.")
