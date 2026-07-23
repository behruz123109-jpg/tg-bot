import aiosqlite
from config import DB_PATH

async def get_user(telegram_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)) as cursor:
            return await cursor.fetchone()

async def add_user(telegram_id: int, full_name: str, username: str, referrer_id: int = None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            INSERT OR IGNORE INTO users (telegram_id, full_name, username, referrer_id)
            VALUES (?, ?, ?, ?)
            """,
            (telegram_id, full_name, username, referrer_id)
        )
        await db.commit()

async def process_tap(telegram_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT coins, energy FROM users WHERE telegram_id = ?", (telegram_id,)) as cursor:
            user = await cursor.fetchone()
            
        if user and user["energy"] > 0:
            new_coins = user["coins"] + 1
            new_energy = user["energy"] - 1
            await db.execute(
                "UPDATE users SET coins = ?, energy = ? WHERE telegram_id = ?",
                (new_coins, new_energy, telegram_id)
            )
            await db.commit()
            return True, new_coins, new_energy
        return False, user["coins"] if user else 0, user["energy"] if user else 0

async def get_setting(key: str) -> str:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT value FROM settings WHERE key = ?", (key,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else ""
