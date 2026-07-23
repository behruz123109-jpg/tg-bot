import aiosqlite
import logging
from config import DB_PATH

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        with open("schema.sql", "r", encoding="utf-8") as f:
            schema = f.read()
        await db.executescript(schema)
        
        # Boshlang'ich dinamik sozlamalar
        default_settings = [
            ("maintenance_mode", "false"),
            ("coin_to_diamond_rate", "10"),
            ("min_withdraw_diamonds", "100"),
            ("ad_reward_diamonds", "3"),
            ("referral_reward_diamonds", "5"),
            ("help_text", "Murojaat va yordam uchun: @admin_username"),
            ("start_text", "O'yinga xush kelibsiz! Tangalarni yig'ing va Olmoslarga almashtiring!")
        ]
        
        for key, val in default_settings:
            await db.execute(
                "INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)",
                (key, val)
            )
            
        await db.commit()
        logging.info("Ma'lumotlar bazasi muvaffaqiyatli ishga tushirildi.")
