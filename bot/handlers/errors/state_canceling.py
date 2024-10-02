import api
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from states import *

# @dp.message_handler(state=[])
# @error_handler()
# async def real_cancellation(message: types.Message, state:FSMContext = None):
#     lang = await api.getUserLanguage(message.from_user.id)
#     if message.text == '/restart':
#         await state.finish()
#         text = await api.getFuncText('cancellation_restart')
#         return await message.answer(
#             text = text[lang],
#             reply_markup=bot_start_keyboard(lang))

#     text = await api.getFuncText('cancellation_try')
#     return await message.answer(text=text[lang])


# @dp.message_handler(commands=['restart'])
# @error_handler()
# async def fake_cancellation(message: types.Message):
#     lang = await api.getUserLanguage(message.from_user.id)
#     text = await api.getFuncText('cancellation_restart')
#     return await message.answer(
#         text = text[lang],
#         reply_markup=bot_start_keyboard(lang)
#     )
