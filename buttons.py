from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu():
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Фото', callback_data='photo'),
            InlineKeyboardButton(text='Подписки', callback_data='subs'),
        ],
        [
            InlineKeyboardButton(text='Техподдержка', callback_data='support'),
        ],
    ])
    return markup


def get_photo_menu():
    photo_key = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Сохраненные фото', callback_data='saved_photo'),
        ],
        [
            InlineKeyboardButton(text='Загрузить фото', callback_data='upload_photo'),
        ],
        [
            InlineKeyboardButton(text='Меню', callback_data='menu'),
            InlineKeyboardButton(text='Назад', callback_data='back1'),
        ],
    ])
    return photo_key


def get_photo_list(photos):
    photo_list = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f"Фото {i+1}", callback_data=f"view_photo:{i}")
            for i, _ in enumerate(photos)
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="photo_menu")
        ]

    ])
    return photo_list


def get_photo_del(photo):
    photo_key2 = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Удалить', callback_data=f'delete:{photo}'),
        ],
        [
            InlineKeyboardButton(text='Меню', callback_data='menu'),
            InlineKeyboardButton(text='Назад', callback_data='photo_menu'),
        ],
    ])
    return photo_key2


def get_subscriptions_menu():
    sub_key = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Мои подписки', callback_data='my_subs'),
        ],
        [
            InlineKeyboardButton(text='Поиск', callback_data='search'),
        ],
        [
            InlineKeyboardButton(text='Меню', callback_data='menu'),
            InlineKeyboardButton(text='Назад', callback_data='menu'),
        ],
    ])
    return sub_key


def get_subscriptions_list(subs):
    buttons = []
    for sub in subs:
        buttons.append([InlineKeyboardButton(text=f"@{sub}", callback_data=f"select_user:{sub}")])
    buttons.append([InlineKeyboardButton(text="Назад", callback_data="back2")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def search_sub_menu():
    sub_key2 = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Подписаться', callback_data='subscribe'),
        ],
        [
            InlineKeyboardButton(text='Меню', callback_data='menu'),
            InlineKeyboardButton(text='Назад', callback_data='back2'),
        ],
    ])
    return sub_key2


def get_profile_menu():
    sub_key3 = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Фото', callback_data='sub_photo'),
        ],
        [
            InlineKeyboardButton(text='Отписаться', callback_data='unsub'),
        ],
        [
            InlineKeyboardButton(text='Меню', callback_data='menu'),
            InlineKeyboardButton(text='Назад', callback_data='back2'),
        ],
    ])
    return sub_key3


def get_support_menu():
    sup_key = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Отправить сообщение', callback_data='sup_mes'),
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data='sup_menu'),
        ],
    ])
    return sup_key


def back_to_menu():
    back_key1 = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Меню', callback_data='menu'),
            InlineKeyboardButton(text='Назад', callback_data='back'),
        ],
    ])
    return back_key1


def get_accept_menu():
    accept_key = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Подтвердить', callback_data='accept'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel'),
        ]
    ])
    return accept_key