from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from loader import bot, dp
from states.profile import ProfileStates


async def delete_last_message(message: types.Message):
    try:
        await message.delete()
    except:
        pass


keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("Отправить номер", request_contact=True))


async def state_finish(state: FSMContext):
    await state.finish()


@dp.message_handler(commands=["start"], state="*")
async def bot_start(message: types.Message, state: FSMContext, user: dict = None):
    await state.finish()

    # проверка профиля
    email = user.get("email", None)
    phone = user.get("phone_number", None)

    if not email:
        await message.answer(
            "Здравствуйте, чтобы полноценно пользоваться ботом, <strong>укажите пожалуйста следующим сообщением Вам E-mail.</strong>\n\n"
            "На данный момент наблюдаются проблемы с работой Telegram, поэтому мы разработали Web App приложение!\n\n"
            "Указав Email - мы сможем связать Ваш текущий телеграмм аккаунт с аккаунтом приложения, и сможем оставаться всегда с Вами на связи!"
        )
        await ProfileStates.waiting_email.set()
        return

    if not phone:
        # await ProfileStates.waiting_phone.set()
        return await message.answer(
            "Укажите пожалуйста номер телефона, нажав кнопку ниже:",
            reply_markup=keyboard,
        )

    msg = (
        f"Добро пожаловать, {message.from_user.first_name}!\n\n"
        "Отправьте фото штрих/QR-кода для добавления заказа.\n\n"
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
