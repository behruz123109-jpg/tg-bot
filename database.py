import sqlite3

DB_NAME = "game_database.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Foydalanuvchilar bazasi
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    coins INTEGER DEFAULT 0,
                    uc_chips INTEGER DEFAULT 0)''')
                    
    # Dinamik Sozlamalar bazasi (Admin o'zgartiradigan barcha parametrlar)
    c.execute('''CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT)''')
                    
    # Vazifalar bazasi
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    reward_amount INTEGER,
                    reward_type TEXT,
                    url TEXT)''')

    # Boshlang'ich sozlamalarni kiritish (Agar yo'q bo'lsa)
    defaults = {
        "admin_card": "8600 0000 0000 0000",
        "card_owner": "ADMIN ISMI",
        "olmos_price": "100",  # 1 Olmos = 100 so'm
        "swap_rate": "100000", # 100k Tanga = 50 Olmos
        "swap_reward": "50"
    }
    for key, val in defaults.items():
        c.execute('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)', (key, val))

    conn.commit()
    conn.close()

def get_setting(key):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT value FROM settings WHERE key = ?', (key,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else ""

def set_setting(key, value):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('UPDATE settings SET value = ? WHERE key = ?', (value, key))
    conn.commit()
    conn.close()

def add_user(user_id, username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)', (user_id, username))
    conn.commit()
    conn.close()

def add_task(title, reward_amount, reward_type, url):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO tasks (title, reward_amount, reward_type, url) VALUES (?, ?, ?, ?)', 
              (title, reward_amount, reward_type, url))
    conn.commit()
    conn.close()

def get_all_tasks():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id, title, reward_amount, reward_type, url FROM tasks')
    rows = c.fetchall()
    conn.close()
    return rows
