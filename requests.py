from db import *


def connect_db():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


def add_user(username, tg_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, tg_id) VALUES (%s, %s) ON CONFLICT (username) DO NOTHING', (username, tg_id))
    conn.commit()
    cursor.close()
    conn.close()


def add_photo(user_id, photo):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO photos (user_id, photo) VALUES (%s, %s)', (user_id, photo))
    conn.commit()
    cursor.close()
    conn.close()


def get_user_photos(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT photo FROM photos WHERE user_id = %s', (user_id,))
    photos = cursor.fetchall()
    cursor.close()
    conn.close()
    return [photo[0] for photo in photos]


def update_number(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT photo_id FROM photos WHERE user_id = %s ORDER BY number', (user_id,))
    photos = cursor.fetchall()
    for new_number, photo in enumerate(photos, start=1):
        photo_id = photo[0]
        cursor.execute('UPDATE photos SET number = %s WHERE photo_id = %s', (new_number, photo_id))
    conn.commit()
    cursor.close()
    conn.close()


def remove_photo(user_id, number):
    conn = connect_db()
    cursor = conn.cursor()
    update_number(user_id)
    cursor.execute('SELECT photo FROM photos WHERE user_id = %s AND number = %s', (user_id, number,))
    result = cursor.fetchone()
    photo_path = result[0]
    cursor.execute('DELETE FROM photos WHERE user_id = %s AND number = %s', (user_id, number))
    conn.commit()
    cursor.close()
    conn.close()
    os.remove(photo_path)


def add_subscription(sub_username, user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO subscriptions (sub_username, user_id) VALUES (%s, %s)
                   ON CONFLICT(sub_username) DO UPDATE SET user_id = excluded.user_id''', (sub_username, user_id))
    conn.commit()
    cursor.close()
    conn.close()


def get_user_subscriptions(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT sub_username FROM subscriptions WHERE user_id = %s', (user_id,))
    subscriptions = cursor.fetchall()
    cursor.close()
    conn.close()
    return [subscription[0] for subscription in subscriptions]


def get_user_id(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM users WHERE username = %s', (username,))
    user_id = cursor.fetchone()
    cursor.close()
    conn.close()
    return user_id[0] if user_id else None


def is_valid_username(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM users WHERE username = %s', (username,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return bool(count)


def subscribe_user(user_id, username):
    if is_valid_username(username):
        add_subscription(username, user_id)


def unsubscribe_user(user_id, sub_username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM subscriptions WHERE user_id = %s AND sub_username = %s', (user_id, sub_username))
    conn.commit()
    cursor.close()
    conn.close()


def get_all_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT tg_id, username FROM users')
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{'tg_id': user[0],  'username': user[1]} for user in users]
