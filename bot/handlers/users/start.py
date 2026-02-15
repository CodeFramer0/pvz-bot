from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import bot, dp
from states.profile import ProfileStates


async def delete_last_message(message: types.Message):
    try:
        await message.delete()
    except:
        pass


async def state_finish(state: FSMContext):
    await state.finish()


@dp.message_handler(commands=["start"], state="*")
async def bot_start(message: types.Message, state: FSMContext, user: dict = None):
    await state.finish()

    # проверка профиля
    app_user = user.get("app_user") if user else None
    email = app_user.get("email") if isinstance(app_user, dict) else None
    phone = user.get("phone_number") if user else None
    phone = user.get("phone_number") if user else None

    if not email:
        await ProfileStates.waiting_email.set()
        await message.answer(
            "Здравствуйте, чтобы полноценно пользоваться ботом, <strong>укажите пожалуйста следующим сообщением Вам E-mail.</strong>\n\n"
            "На данный момент наблюдаются проблемы с работой Telegram, поэтому мы разработали Web App приложение!\n\n"
            "Указав Email - мы сможем связать Ваш текущий телеграмм аккаунт с аккаунтом приложения, и сможем оставаться всегда с Вами на связи!"
        )
        return

    if not phone:
        # await ProfileStates.waiting_phone.set()
        await message.answer("Укажи номер телефона (в формате +79990000000):")
        return

    msg = (
        f"Добро пожаловать, {message.from_user.first_name}!\n\n"
        "Пришли фото штрих/QR-кода для добавления заказа.\n\n"
        "Разработчик @CodeFramer (по тех. вопросам)."
    )
    await message.answer(msg)


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
