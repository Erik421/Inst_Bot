"""
Create tables users, photos, subscriptions
"""

from yoyo import step

__depends__ = {}


steps = [
    step("""
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            tg_id BIGINT NOT NULL,
            username VARCHAR(255) UNIQUE
        )
    """),
    step("""
        CREATE TABLE IF NOT EXISTS photos (
            photo_id SERIAL PRIMARY KEY,
            user_id INTEGER,
            photo TEXT NOT NULL,
            number INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
        )
    """),
    step("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            subscription_id SERIAL PRIMARY KEY,
            sub_username VARCHAR(255) UNIQUE,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
        )
    """)
]
