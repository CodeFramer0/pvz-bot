from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp
from utils.utils import delete_last_message,delete_message
from utils.utils import state_finish

@dp.message_handler(CommandStart(),state="*")
async def bot_start(message: types.Message,user,state:FSMContext):
    await state_finish(state)
    data = await state.get_data()
    if data:
        await delete_message(chat_id=user["user_id"], message_id=data.get("message_id"))
    await message.answer(
        f"Добро пожаловать, {message.from_user.first_name}! 🤖\n"
        "Я бот для заказа доставки из пункта выдачи.\n\n"
        "Пожалуйста, пришлите мне фото Вашего штрих/QR-кода, чтобы я мог добавить его в список заказов. 📦\n\n"
        "Разработчик @CodeFramer (<strong>по техническим вопросам</strong>).\n\n"
    )



async def back_to_main_menu(message: types.Message, user: dict, state: FSMContext):
    await delete_last_message(message)
    data = await state.get_data()
    if data:
        await delete_message(chat_id=user["user_id"], message_id=data.get("message_id"))
    await bot_start(message,user,state)
