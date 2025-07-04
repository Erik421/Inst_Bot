from db import *


async def add_user(username, user_id):
    conn = await connect_db()
    await conn.execute('''
        INSERT INTO users (username, user_id) VALUES ($1, $2)
        ON CONFLICT (username) DO NOTHING
    ''', username, user_id)
    await conn.close()


async def add_photo(user_id, photo):
    conn = await connect_db()
    await conn.execute('''
        INSERT INTO photos (user_id, photo) VALUES ($1, $2)
    ''', user_id, photo)
    await conn.close()


async def get_user_photos(user_id):
    conn = await connect_db()
    photos = await conn.fetch('''
        SELECT photo FROM photos WHERE user_id = $1
    ''', user_id)
    await conn.close()
    return [photo['photo'] for photo in photos]


async def remove_photo(user_id, photo):
    conn = await connect_db()
    photo_path = await conn.fetchval('''
        SELECT photo FROM photos WHERE user_id = $1 AND photo = $2
    ''', user_id, photo)
    if photo_path:
        await conn.execute('''
            DELETE FROM photos WHERE user_id = $1 AND photo = $2
        ''', user_id, photo)
        os.remove(photo_path)
    await conn.close()


async def add_subscription(sub_username, user_id):
    conn = await connect_db()
    await conn.execute('''
        INSERT INTO subscriptions (sub_username, user_id) VALUES ($1, $2)
        ON CONFLICT (sub_username) DO UPDATE SET user_id = excluded.user_id
    ''', sub_username, user_id)
    await conn.close()


async def get_user_subscriptions(user_id):
    conn = await connect_db()
    subscriptions = await conn.fetch('''
        SELECT sub_username FROM subscriptions WHERE user_id = $1
    ''', user_id)
    await conn.close()
    return [subscription['sub_username'] for subscription in subscriptions]


async def get_user_id(username):
    conn = await connect_db()
    user_id = await conn.fetchval('''
        SELECT user_id FROM users WHERE username = $1
    ''', username)
    await conn.close()
    return user_id


async def is_valid_username(username):
    conn = await connect_db()
    count = await conn.fetchval('''
        SELECT COUNT(*) FROM users WHERE username = $1
    ''', username)
    await conn.close()
    return bool(count)


async def subscribe_user(user_id, username):
    if await is_valid_username(username):
        await add_subscription(username, user_id)


async def unsubscribe_user(user_id, sub_username):
    conn = await connect_db()
    await conn.execute('''
        DELETE FROM subscriptions WHERE user_id = $1 AND sub_username = $2
    ''', user_id, sub_username)
    await conn.close()


async def get_all_users():
    conn = await connect_db()
    users = await conn.fetch('''
        SELECT user_id, username FROM users
    ''')
    await conn.close()
    return [{'user_id': user['user_id'], 'username': user['username']} for user in users]