from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(
        f"Добро пожаловать, {message.from_user.first_name}! 🤖\n"
        "Я бот для заказа доставки из пункта выдачи.\n\n"
        "Пожалуйста, пришлите мне фото Вашего штрих/QR-кода, чтобы я мог добавить его в список заказов. 📦\n\n"
        "Разработчик @CodeFramer (<strong>по техническим вопросам</strong>).\n\n"
        'P.S. Если Вы считаете, что бот не работает, скорее всего, Вы не завершили процесс создания заказа. Все, что Вам нужно, это нажать на кнопку "Отменить ❌" или ввести команду "/cancel".'
    )
