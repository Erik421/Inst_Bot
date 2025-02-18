# import os
# from dotenv import load_dotenv
# import asyncpg
#
#
# load_dotenv()
#
# DB_NAME = os.getenv('DB_NAME')
# DB_USER = os.getenv('DB_USER')
# DB_PASSWORD = os.getenv('DB_PASSWORD')
# DB_HOST = os.getenv('DB_HOST')
# DB_PORT = os.getenv('DB_PORT')
#
#
# async def init_db():
#     conn = await asyncpg.connect(
#         database=DB_NAME,
#         user=DB_USER,
#         password=DB_PASSWORD,
#         host=DB_HOST,
#         port=DB_PORT,
#     )
#
#
#     await conn.execute('''
#         CREATE TABLE IF NOT EXISTS users (
#             user_id SERIAL PRIMARY KEY,
#             tg_id BIGINT NOT NULL,
#             username VARCHAR(255) UNIQUE
#         )
#     ''')
#
#
#     await conn.execute('''
#         CREATE TABLE IF NOT EXISTS photos (
#             photo_id SERIAL PRIMARY KEY,
#             user_id INTEGER,
#             photo TEXT NOT NULL,
#             number INTEGER,
#             FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
#         )
#     ''')
#
#
#     await conn.execute('''
#         CREATE TABLE IF NOT EXISTS subscriptions (
#             subscription_id SERIAL PRIMARY KEY,
#             sub_username VARCHAR(255) UNIQUE,
#             user_id INTEGER,
#             FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
#         )
#     ''')
#
#     await conn.close()
