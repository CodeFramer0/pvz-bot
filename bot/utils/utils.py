import re

from aiogram.dispatcher import FSMContext
from loader import bot


async def delete_message(chat_id, message_id):
    try:
        await bot.delete_message(chat_id, message_id)
    except:
        pass


async def delete_last_message(message):
    try:
        await message.delete()
    except:
        pass


async def state_finish(state: FSMContext):
    try:
        await state.finish()
    except:
        pass
