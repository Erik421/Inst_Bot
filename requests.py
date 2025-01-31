from db import *


def add_user(username, tg_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (username, tg_id) VALUES (?, ?)', (username, tg_id))
    conn.commit()
    conn.close()


def add_photo(user_id, photo):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO photos (user_id, photo) VALUES (?, ?)', (user_id, photo))
    conn.commit()
    conn.close()


def get_user_photos(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT photo FROM photos WHERE user_id = ?', (user_id,))
    photos = cursor.fetchall()
    conn.close()
    return [photo[0] for photo in photos]


def update_number(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT photo_id FROM photos WHERE user_id = ? ORDER BY number', (user_id,))
    photos = cursor.fetchall()
    for new_number, photo in enumerate(photos, start=1):
        photo_id = photo[0]
        cursor.execute('UPDATE photos SET number = ? WHERE photo_id = ?', (new_number, photo_id))
    conn.commit()
    conn.close()


def remove_photo(user_id, number):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    update_number(user_id)
    cursor.execute('SELECT photo FROM photos WHERE user_id = ? AND number = ?', (user_id, number,))
    result = cursor.fetchone()
    photo_path = result[0]
    cursor.execute('DELETE FROM photos WHERE user_id = ? AND number = ?', (user_id, number))
    # update_number(user_id)
    conn.commit()
    conn.close()
    os.remove(photo_path)


def add_subscription(sub_username, user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO subscriptions (sub_username, user_id) VALUES (?, ?)'
                   'ON CONFLICT(sub_username) DO UPDATE SET user_id = excluded.user_id', (sub_username, user_id))
    conn.commit()
    conn.close()


def get_user_subscriptions(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT sub_username FROM subscriptions WHERE user_id = ?', (user_id,))
    subscriptions = cursor.fetchall()
    conn.close()
    return [subscription[0] for subscription in subscriptions]


def get_user_id(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM users WHERE username = ?', (username,))
    user_id = cursor.fetchone()
    conn.close()
    return user_id[0] if user_id else None


def is_valid_username(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', (username,))
    count = cursor.fetchone()[0]
    conn.close()
    return bool(count)


def subscribe_user(user_id, username):
    if is_valid_username(username):
        add_subscription(username, user_id)


def unsubscribe_user(user_id, sub_username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM subscriptions WHERE user_id = ? AND sub_username = ?', (user_id, sub_username))
    conn.commit()
    conn.close()


def get_all_users():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT tg_id FROM users')
    users = cursor.fetchall()
    conn.close()
    return [{'tg_id': user[0]} for user in users]
