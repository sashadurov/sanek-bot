import sqlite3
import json
from datetime import datetime

DB_PATH = "bandit.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            balance INTEGER DEFAULT 1000,
            level INTEGER DEFAULT 1,
            xp INTEGER DEFAULT 0,
            job TEXT DEFAULT NULL,
            job_last_used INTEGER DEFAULT 0,
            businesses TEXT DEFAULT \"{}\",
            houses TEXT DEFAULT \"[]\",
            cars TEXT DEFAULT \"[]\",
            clothes TEXT DEFAULT \"[]\",
            created_at TEXT
        )
    ''')

    conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row

def create_user(user_id, username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT OR IGNORE INTO users (user_id, username, created_at) VALUES (?, ?, ?)",
        (user_id, username, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def update_balance(user_id, amount):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    conn.close()

def set_job(user_id, job_key):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET job = ? WHERE user_id = ?", (job_key, user_id))
    conn.commit()
    conn.close()

def set_job_cooldown(user_id, timestamp):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET job_last_used = ? WHERE user_id = ?", (timestamp, user_id))
    conn.commit()
    conn.close()

def add_business(user_id, business_key):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT businesses FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    businesses = json.loads(row[0]) if row and row[0] else {}
    if business_key not in businesses:
        businesses[business_key] = {"last_collected": 0}
    c.execute("UPDATE users SET businesses = ? WHERE user_id = ?", (json.dumps(businesses), user_id))
    conn.commit()
    conn.close()

def update_business_cooldown(user_id, business_key, timestamp):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT businesses FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    businesses = json.loads(row[0]) if row and row[0] else {}
    if business_key in businesses:
        businesses[business_key]["last_collected"] = timestamp
    c.execute("UPDATE users SET businesses = ? WHERE user_id = ?", (json.dumps(businesses), user_id))
    conn.commit()
    conn.close()

def add_item(user_id, item_type, item_key):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    column = item_type + "s"  # houses, cars, clothes
    c.execute(f"SELECT {column} FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    items = json.loads(row[0]) if row and row[0] else []
    if item_key not in items:
        items.append(item_key)
    c.execute(f"UPDATE users SET {column} = ? WHERE user_id = ?", (json.dumps(items), user_id))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_id, username, balance, level FROM users ORDER BY balance DESC LIMIT 20")
    rows = c.fetchall()
    conn.close()
    return rows
