import os
import sqlite3

DB_NAME = 'inst_bot.db'
if not os.path.exists('photos'):
    os.makedirs('photos')


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id INTEGER NOT NULL,
            username TEXT UNIQUE
        )
    ''')
    conn.commit()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS photos (
            photo_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            photo TEXT NOT NULL,
            number INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    conn.commit()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscriptions (
            subscription_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sub_username TEXT UNIQUE,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')


