import aiosqlite
import logging

# Ma'lumotlar bazasi fayli nomi (LibSQL/SQLite formatida)
DB_NAME = "bot_database.db"

async def init_db():
    """Barcha jadvallarni va boshlang'ich sozlamalarni yaratish"""
    async with aiosqlite.connect(DB_NAME) as db:
        
        # 1. FOYDALANUVCHILAR (Users)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                coins INTEGER DEFAULT 0,
                diamonds INTEGER DEFAULT 0,
                energy INTEGER DEFAULT 1000,
                max_energy INTEGER DEFAULT 1000,
                level INTEGER DEFAULT 1,
                referrer_id INTEGER,
                is_banned BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 2. DINAMIK SOZLAMALAR (Admin panel uchun)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                setting_key TEXT PRIMARY KEY,
                setting_value TEXT
            )
        """)
        
        # Boshlang'ich sozlamalarni kiritib qo'yamiz (agar yo'q bo'lsa)
        default_settings = [
            ('help_text', 'Bot qoidalari va yordam matni. Admin buni o\'zgartirishi mumkin.'),
            ('start_text', 'Asosiy menyuga xush kelibsiz!'),
            ('maintenance_mode', '0'), # 1 qilsangiz bot texnik tanaffusga tushadi
            ('min_payout', '100'), # Yechish uchun minimal olmos
            ('diamond_to_uc_rate', '60') # 100 Olmos = 60 UC
        ]
        await db.executemany(
            "INSERT OR IGNORE INTO settings (setting_key, setting_value) VALUES (?, ?)",
            default_settings
        )

        # 3. TO'LOVLAR VA KASSA (Payouts)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS payouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                diamonds_spent INTEGER NOT NULL,
                amount_type TEXT, -- 'UC', 'SUM', 'CARD'
                details TEXT,     -- PUBGM ID yoki Karta raqami
                status TEXT DEFAULT 'pending', -- pending, approved, rejected
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(telegram_id)
            )
        """)

        # 4. VAZIFALAR VA HOMIYLAR (Tasks)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                task_type TEXT, -- channel, story, quiz
                reward_diamonds INTEGER DEFAULT 0,
                reward_coins INTEGER DEFAULT 0,
                url TEXT,
                is_active BOOLEAN DEFAULT 1
            )
        """)

        # 5. BAJARILGAN VAZIFALAR (User Tasks)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS user_tasks (
                user_id INTEGER,
                task_id INTEGER,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, task_id),
                FOREIGN KEY(user_id) REFERENCES users(telegram_id),
                FOREIGN KEY(task_id) REFERENCES tasks(id)
            )
        """)

        await db.commit()
        logging.info("✅ Ma'lumotlar bazasi muvaffaqiyatli ishga tushdi va jadvallar yangilandi!")

# --- Bazaga ulanish uchun yordamchi funksiyalar (API) ---

async def add_user(telegram_id, username, full_name, referrer_id=None):
    """Yangi foydalanuvchini ro'yxatdan o'tkazish"""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT OR IGNORE INTO users (telegram_id, username, full_name, referrer_id)
            VALUES (?, ?, ?, ?)
        """, (telegram_id, username, full_name, referrer_id))
        await db.commit()

async def get_setting(key):
    """Admin sozlamalarini o'qish (Bot to'xtamasligi uchun)"""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT setting_value FROM settings WHERE setting_key = ?", (key,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None
