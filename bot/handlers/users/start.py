from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import bot, dp


async def delete_last_message(message: types.Message):
    try:
        await message.delete()
    except:
        pass


async def state_finish(state: FSMContext):
    await state.finish()


@dp.message_handler(commands=["start"], state="*")
async def bot_start(message: types.Message, state: FSMContext, user: dict = None):
    # Завершаем текущее состояние
    await state_finish(state)

    # Удаляем старое сообщение
    data = await state.get_data()
    if data and "message_id" in data:
        try:
            await bot.delete_message(
                chat_id=user["user_id"], message_id=data["message_id"]
            )
        except:
            pass

    # Приветствие
    msg = (
        f"Добро пожаловать, {message.from_user.first_name}! 🤖\n"
        "Я бот для заказа доставки из пункта выдачи.\n\n"
        "Пожалуйста, пришлите мне фото Вашего штрих/QR-кода, чтобы я мог добавить его в список заказов. 📦\n\n"
        "Разработчик @CodeFramer (<strong>по техническим вопросам</strong>).\n\n"
    )
    sent = await message.answer(msg)
    await state.update_data(message_id=sent.message_id)


async def back_to_main_menu(message: types.Message, state: FSMContext, user: dict):
    await delete_last_message(message)
    data = await state.get_data()
    if data and "message_id" in data:
        try:
            await bot.delete_message(
                chat_id=user["user_id"], message_id=data["message_id"]
            )
        except:
            pass
    await bot_start(message, state, user=user)
