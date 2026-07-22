import sqlite3

DB_NAME = "game_database.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    coins INTEGER DEFAULT 0,
                    uc_chips INTEGER DEFAULT 0,
                    joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
                    
    c.execute('''CREATE TABLE IF NOT EXISTS channels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    channel_username TEXT UNIQUE,
                    title TEXT)''')
                    
    c.execute('''CREATE TABLE IF NOT EXISTS withdrawals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    chips INTEGER,
                    pubg_id TEXT,
                    status TEXT DEFAULT 'Kutilmoqda')''')
    conn.commit()
    conn.close()

def add_user(user_id, username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)', (user_id, username))
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM users')
    total_users = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM withdrawals WHERE status = "Kutilmoqda"')
    pending_w = c.fetchone()[0]
    conn.close()
    return total_users, pending_w

def get_all_users():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT user_id FROM users')
    users = [row[0] for row in c.fetchall()]
    conn.close()
    return users

def add_channel(username, title):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute('INSERT INTO channels (channel_username, title) VALUES (?, ?)', (username, title))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_channels():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id, channel_username, title FROM channels')
    rows = c.fetchall()
    conn.close()
    return rows

def delete_channel(channel_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM channels WHERE id = ?', (channel_id,))
    conn.commit()
    conn.close()

def add_withdrawal(user_id, chips, pubg_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO withdrawals (user_id, chips, pubg_id) VALUES (?, ?, ?)', (user_id, chips, pubg_id))
    conn.commit()
    conn.close()

def get_pending_withdrawals():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id, user_id, chips, pubg_id FROM withdrawals WHERE status = "Kutilmoqda"')
    rows = c.fetchall()
    conn.close()
    return rows

def update_withdrawal_status(wid, status):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('UPDATE withdrawals SET status = ? WHERE id = ?', (status, wid))
    conn.commit()
    conn.close()

def add_chips(user_id, amount):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('UPDATE users SET uc_chips = uc_chips + ? WHERE user_id = ?', (amount, user_id))
    conn.commit()
    conn.close()
