from aiogram.dispatcher.filters.state import State, StatesGroup


class ProfileStates(StatesGroup):
    waiting_email = State()
    waiting_phone = State()
