import os
import psycopg2


DB_NAME = 'inst_bot'
DB_USER = 'Erik'
DB_PASSWORD = '12456'
DB_HOST = '127.0.0.1'
DB_PORT = '5432'

if not os.path.exists('photos'):
    os.makedirs('photos')


def init_db():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        # options="-c client_encoding=UTF8"
    )
    cursor = conn.cursor()


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            tg_id BIGINT NOT NULL,
            username VARCHAR(255) UNIQUE
        )
    ''')
    conn.commit()


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS photos (
            photo_id SERIAL PRIMARY KEY,
            user_id INTEGER,
            photo TEXT NOT NULL,
            number INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
        )
    ''')
    conn.commit()


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscriptions (
            subscription_id SERIAL PRIMARY KEY,
            sub_username VARCHAR(255) UNIQUE,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
        )
    ''')
    conn.commit()

    cursor.close()
    conn.close()
