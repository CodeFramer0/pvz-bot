from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from loader import auth_api, dp, telegram_user_api, users_api
from states.profile import ProfileStates


@dp.message_handler(commands=["profile"], state="*")
async def profile_command(message: Message, user: dict):
    """
    Показываем профиль Telegram-пользователя.
    `user` берется из middleware (UserProfileMiddleware)
    """
    if not user:
        await message.answer("Пользователь не найден в базе 😕")
        return
    msg = (
        f"👤 <b>Ваш профиль</b>:\n\n"
        f"Имя: {user.get('name', 'NoName')}\n"
        f"Ник: {user.get('nick_name', 'NoName')}\n"
        f"E-mail: {user.get('email', ' ')}\n"
        f"Номер телефона: {user.get('phone_number', ' ')}\n"
        f"Telegram ID: {user.get('user_id')}\n"
        f"Заблокирован: {'Да' if user.get('is_blocked') else 'Нет'}\n"
        f"Администратор: {'Да' if user.get('is_administrator') else 'Нет'}\n"
        f"Дата регистрации: {user.get('date_join', '—')}"
    )

    await message.answer(msg, parse_mode="HTML")


@dp.message_handler(state=ProfileStates.waiting_email)
async def set_email(message: Message, state: FSMContext, user: dict):
    email = message.text.strip()
    if "@" not in email:
        await message.answer("Это не похоже на email. Попробуй ещё раз:")
        return

    await auth_api.send_verification_code(email=email)
    await state.update_data(email=email)
    await message.answer("✅ Код отправлен на ваш email. Введите его сюда:")
    await ProfileStates.waiting_verification_code.set()


@dp.message_handler(state=ProfileStates.waiting_verification_code)
async def verify_code(message: Message, state: FSMContext, user: dict):
    data = await state.get_data()
    email = data.get("email")
    code = message.text.strip()

    # Проверяем код через API
    result = await auth_api.verify_code(email=email, code=code)
    if not result or not result.get("temporary_token"):
        await message.answer("❌ Неверный код. Попробуйте ещё раз:")
        return

    temp_token = result["temporary_token"]

    # Привязываем AppUser к TelegramUser
    bind_result = await telegram_user_api.bind_user(id=user["id"], email=email)
    if not bind_result:
        await message.answer("Ошибка при привязке профиля. Попробуйте позже.")
        return

    await message.answer(
        f"✅ Профиль успешно создан и привязан!\n\n"
        f"Email:<code>{bind_result['email']}</code>\n"
        f"Пароль: <code>{bind_result['password']}</code>\n\n"
    )
    await state.finish()


@dp.message_handler(content_types=["contact"])
async def handle_contact(message: types.Message, user: dict):
    if not message.contact:
        await message.answer("Контакт не получен.")
        return

    if message.contact.user_id != message.from_user.id:
        await message.answer("Можно отправлять только свой номер!")
        return

    phone_number = message.contact.phone_number

    result = await users_api.patch(
        id=user["app_user"], json={"phone_number": phone_number}
    )

    if result:
        await message.answer(
            f"Ваш номер {phone_number} успешно привязан к аккаунту",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await message.answer(
            "Ошибка при привязке номера через API.", reply_markup=ReplyKeyboardRemove()
        )
    await message.answer(result)
