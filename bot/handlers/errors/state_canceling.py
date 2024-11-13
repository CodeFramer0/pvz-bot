import api
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from states.order import OrderStates


@dp.message_handler(
    state=[
        OrderStates.waiting_for_marketplace,
        OrderStates.waiting_for_pickup_point,
        
    ]
)
async def real_cancellation(message: types.Message,state:FSMContext):
    if message.text == "/cancel":
        await state.finish()
        await message.answer(
            f"Состояние успешно отменено, жду Ваш штрих/QR-код 🤖.\n"
            "Я бот для заказа доставки из пункта выдачи.\n\n"
            "Пожалуйста, пришлите фото Вашего штрих/QR-кода, чтобы я мог добавить его в список заказов. 📦\n\n"
            "Разработчик @CodeFramer (<strong>по техническим вопросам</strong>).\n\n"
            'P.S. Если Вы считаете, что бот не работает, скорее всего Вы не завершили процесс создания заказа. Вам нужно нажать на кнопку "Отменить ❌" или ввести команду "/cancel".'
        )
    else:
        await message.answer(
            'Вы находитесь в процессе создания заказа. Бот ожидает от Вас выбора одной из кнопок на клавиатуре (сообщение выше). Пожалуйста, выберите одну из этих кнопок. Если хотите отменить создание заказа, нажмите на кнопку "Отменить" или введите команду "/cancel".'
        )


@dp.message_handler(commands=["cancel"])
async def fake_cancellation(message: types.Message):
    await message.answer(
        f"Состояние успешно отменено, жду Ваш штрих/QR-код 🤖.\n"
        "Я бот для заказа доставки из пункта выдачи.\n\n"
        "Пожалуйста, пришлите фото Вашего штрих/QR-кода, чтобы я мог добавить его в список заказов. 📦\n\n"
        "Разработчик @CodeFramer (<strong>по техническим вопросам</strong>).\n\n"
        'P.S. Если Вы считаете, что бот не работает, скорее всего Вы не завершили процесс создания заказа. Вам нужно нажать на кнопку "Отменить ❌" или ввести команду "/cancel".'
    )
