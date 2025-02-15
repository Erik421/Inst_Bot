import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State

from buttons import *
from requests import *


TOKEN = '7343306090:AAGYlEIBVwE9heIzPr54kWwTBXbVBFKVD3E'
ADMIN_ID = '550649516'


bot = Bot(token=TOKEN)
dp = Dispatcher()


class Exp(StatesGroup):
    upload_photo = State()
    support_message = State()
    admin_message = State()
    del_photo = State()
    sub_message = State()
    select_user = State()
    confirm_unsub = State()



@dp.message(Command('start'))
async def start(message: Message):
    if len(get_all_users()) < 500:
        add_user(message.from_user.username, message.from_user.id)
        await message.answer('Главное меню:', reply_markup=get_main_menu())
    else:
        await message.answer('Бот может зарегистрировать не больше 500 пользователей.')


# Меню "Фото"
@dp.callback_query(lambda c: c.data == 'photo')
async def photo_callback(callback_query: CallbackQuery):
    await callback_query.message.answer('Фото:', reply_markup=get_photo_menu())


@dp.callback_query(lambda c: c.data == 'menu')
async def menu1_callback(callback_query: CallbackQuery):
    await callback_query.message.answer('Главное меню: ', reply_markup=get_main_menu())


@dp.callback_query(lambda c: c.data == 'back1')
async def back1_callback(callback_query: CallbackQuery):
    await callback_query.message.answer('Главное меню: ', reply_markup=get_main_menu())

# Просмотр сохранённых фото
@dp.callback_query(lambda c: c.data == 'saved_photo')
async def saved_photo_callback(callback_query: CallbackQuery):
    username = callback_query.from_user.username
    user_id = get_user_id(username)
    photos = get_user_photos(user_id)
    if not photos:
        await callback_query.message.answer('У вас нет сохраненных фото.')
        await callback_query.message.answer('Фото:', reply_markup=get_photo_menu())
    photo_list_keyboard = get_photo_list(photos)
    await callback_query.message.answer('Выберите фото:', reply_markup=photo_list_keyboard)


@dp.callback_query(lambda c: c.data.startswith('view_photo:'))
async def view_photo_callback(callback_query: CallbackQuery):
    _, photo = callback_query.data.split(':')
    photo = int(photo)
    username = callback_query.from_user.username
    user_id = get_user_id(username)
    photos = get_user_photos(user_id)
    if photos:
        photo_path = photos[photo]
        photo_file = FSInputFile(photo_path)
        await callback_query.message.answer_photo(photo_file, reply_markup=get_photo_del())
    else:
        await callback_query.message.answer('У вас нет сохраненных фото.')
        await callback_query.message.answer('Фото:', reply_markup=get_photo_menu())


@dp.callback_query(lambda c: c.data == 'photo_menu')
async def photo_menu_callback(callback_query: CallbackQuery):
    await callback_query.message.answer('Фото: ', reply_markup=get_photo_menu())

# Загрузка нового фото
@dp.callback_query(lambda c: c.data == 'upload_photo')
async def upload_photo_callback(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Пожалуйста, отправьте ваше фото.")
    await state.set_state(Exp.upload_photo)

@dp.message(Exp.upload_photo)
async def cmd_upload_photo(message: Message):
    username = message.from_user.username
    user_id = get_user_id(username)
    if message.photo:
        if len(get_user_photos(user_id)) < 10:
            file_id = message.photo[-1].file_id
            file = await bot.get_file(file_id)
            photo_path = f"photos/{user_id}_{file_id}.jpg"
            await bot.download_file(file.file_path, photo_path)
            add_photo(user_id, photo_path)
            await message.answer("Фото сохранено!")
        else:
            await message.answer("Вы можете сохранить только до 10 фото.")
        await message.answer('Выберите действие;', reply_markup=get_photo_del())
    else:
        await message.answer("Пожалуйста, отправьте фотографию.")


# Удаление фотографии
@dp.callback_query(lambda c: c.data == 'delete')
async def delete_photo_callback(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer("Какую фотографию вы хотите удалить?")
    await state.set_state(Exp.del_photo)


@dp.message(Exp.del_photo)
async def process_delete_photo(message: Message, state: FSMContext):
    username = message.from_user.username
    user_id = get_user_id(username)
    try:
        number = int(message.text.strip())
        remove_photo(user_id, number)
        await message.answer(f"Фотография {number} удалена.")
    except Exception as e:
        await message.answer(f"Произошла ошибка при удалении фотографии: {e}")
    await message.answer('Выберите действие:', reply_markup=get_photo_del())


# Меню "Подписки"
@dp.callback_query(lambda c: c.data == 'subs')
async def subs_callback(callback_query: CallbackQuery):
    await callback_query.message.answer('Подписки:', reply_markup=get_subscriptions_menu())


# Мои подписки
@dp.callback_query(lambda c: c.data == 'my_subs')
async def my_subs_callback(callback_query: CallbackQuery, state: FSMContext):
    username = callback_query.from_user.username
    user_id = get_user_id(username)
    subs = get_user_subscriptions(user_id)
    if not subs:
        await bot.send_message(callback_query.from_user.id, "У вас нет подписок.")
        await bot.send_message(callback_query.from_user.id, 'Подписки', reply_markup=get_subscriptions_menu())
    else:
        await callback_query.message.answer("Выберите пользователя:", reply_markup=get_subscriptions_list(subs))
        await state.set_state(Exp.select_user)


# Поиск подписчиков
@dp.callback_query(lambda c: c.data == 'search')
async def search_callback(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Введите имя пользователя, на которого хотите подписаться:')
    await state.set_state(Exp.sub_message)


@dp.message(Exp.sub_message)
async def process_search(message: Message, state: FSMContext):
    sub_username = message.text.strip()
    username = message.from_user.username
    user_id = get_user_id(username)
    if len(get_user_subscriptions(user_id)) < 20:
        if is_valid_username(sub_username):
            subscribe_user(user_id, sub_username)
            await message.answer(f"Теперь вы подписаны на @{sub_username}.")
        else:
            await message.answer(f"Не удалось найти пользователя с именем @{sub_username}. Попробуйте еще раз.")
    else:
        await message.answer("Вы можете подписаться только на 20 пользователей.")
    await state.clear()
    await message.answer('Подписки:', reply_markup=get_subscriptions_menu())


@dp.callback_query(lambda c: c.data.startswith('select_user:'))
async def process_select_user(callback_query: CallbackQuery, state: FSMContext):
    sub_username = callback_query.data.split(':')[1]
    await state.update_data(selected_user=sub_username)
    await callback_query.message.answer(f"Вы выбрали @{sub_username}. Что вы хотите сделать?", reply_markup=get_profile_menu())
    await state.set_state(Exp.confirm_unsub)


# Отключение от подписки
@dp.callback_query(lambda c: c.data == 'unsub')
async def unsub_callback(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    sub_username = data.get('selected_user')
    await callback_query.message.answer(f"Вы уверены, что хотите отписаться от @{sub_username}?", reply_markup=get_accept_menu())
    await state.set_state(Exp.confirm_unsub)


@dp.callback_query(lambda c: c.data == 'accept')
async def process_confirm_unsub(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    sub_username = data.get('selected_user')
    username = callback_query.from_user.username
    user_id = get_user_id(username)
    unsubscribe_user(user_id, sub_username)
    await callback_query.message.answer(f"Вы успешно отписались от @{sub_username}.")
    await callback_query.message.answer('Подписки:', reply_markup=get_subscriptions_menu())
    await state.clear()


@dp.callback_query(lambda c: c.data == 'cancel')
async def process_cancel_unsub(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Подписки:', reply_markup=get_subscriptions_menu())
    await state.clear()


# Просмотр фото подписчика
@dp.callback_query(lambda c: c.data == 'sub_photo')
async def sub_photo_callback(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    username = data.get('selected_user')
    user_id = get_user_id(username)
    photos = get_user_photos(user_id)
    if photos:
        media_group = [InputMediaPhoto(media=FSInputFile(photo)) for photo in photos]
        await callback_query.message.answer_media_group(media_group)
    else:
        await callback_query.message.answer(f"У пользователя @{username} нет фото.")
    await callback_query.message.answer('Подписки:', reply_markup=get_profile_menu())


@dp.callback_query(lambda c: c.data == 'back2')
async def sup_menu_callback(callback_query: CallbackQuery):
    await cmd_sub_menu(callback_query.message)


async def cmd_sub_menu(message:Message):
    await message.answer('Подписки ', reply_markup=get_subscriptions_menu())


# Меню "Техподдержка"
@dp.callback_query(lambda c: c.data == 'support')
async def support_callback(callback_query: CallbackQuery):
    await cmd_sup(callback_query.message)


async def cmd_sup(message: Message):
    await message.answer('Техподдержка:', reply_markup=get_support_menu())


# Отправка сообщения в техподдержку
@dp.callback_query(lambda c: c.data == 'sup_mes')
async def sup_mes_callback(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Напишите свое сообщение:")
    await state.set_state(Exp.support_message)


@dp.message(Exp.support_message)
async def process_support_message(message: Message, state: FSMContext):
    await bot.send_message(ADMIN_ID, f"Сообщение от {message.from_user.full_name}:\n\n{message.text}")
    await message.answer("Ваше сообщение было отправлено в службу поддержки.")
    await state.clear()
    await message.answer('Техподдержка:', reply_markup=get_support_menu())


@dp.callback_query(lambda c: c.data == 'sup_menu')
async def sup_menu_callback(callback_query: CallbackQuery):
    await cmd_sup_menu(callback_query.message)


async def cmd_sup_menu(message: Message):
    await message.answer('Главное меню: ', reply_markup=get_main_menu())


@dp.message(Command('admin'))
async def broadcast_command(message: Message, state: FSMContext):
    if str(message.from_user.id) != ADMIN_ID:
        await message.reply("Эта команда доступна только для администратора.")
        return
    await message.answer("Введите текст сообщения для рассылки:")
    await state.set_state(Exp.admin_message)


@dp.message(Exp.admin_message)
async def process_broadcast_message(message: Message, state: FSMContext):
    text = message.text
    users = get_all_users()
    successful_users = []
    failed_users = []
    for user in users:
        try:
            await bot.send_message(user['tg_id'], text)
            successful_users.append(user['username'])
        except Exception as e:
            failed_users.append((user['username'], str(e)))
    success_message = "Сообщение успешно отправлено следующим пользователям:\n" + "\n".join(
            [f"@{username}" for username in successful_users])
    if failed_users:
        failure_message = "Произошли ошибки при отправке сообщений следующим пользователям:\n" + "\n".join(
            [f"@{username}: {error}" for username, error in failed_users])
    else:
        failure_message = ""
    admin_message = success_message
    if failure_message:
        admin_message += "\n\n" + failure_message
    await bot.send_message(ADMIN_ID, admin_message)
    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    init_db()
    asyncio.run(main())
