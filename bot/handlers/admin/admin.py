from aiogram import types
from loader import dp
from utils.misc.throttling import rate_limit


@rate_limit(limit=1)
@dp.message_handler(commands=["id"])
async def get_chat_id(message: types.Message):
    return await message.answer(message.chat.id)
