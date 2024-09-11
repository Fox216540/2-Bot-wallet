from aiogram.dispatcher.filters.state import State, StatesGroup

class Mailing(StatesGroup):
    message = State()

class change(StatesGroup):
    message = State()

class change2(StatesGroup):
    message = State()

class wallet(StatesGroup):
    wallet_user = State()
    message = State()

class Channels(StatesGroup):
    channel = State()

class well(StatesGroup):
    message = State()

class Trash(StatesGroup):
    message = State()