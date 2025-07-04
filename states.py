from aiogram.fsm.state import StatesGroup, State


class Exp(StatesGroup):
    upload_photo = State()
    support_message = State()
    admin_message = State()
    sub_message = State()
