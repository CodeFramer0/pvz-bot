from aiogram.dispatcher.filters.state import State, StatesGroup


class OrderStates(StatesGroup):
    waiting_for_full_name = State()
    waiting_for_marketplace = State()
    waiting_for_pickup_point = State()
    waiting_for_comment = State()
