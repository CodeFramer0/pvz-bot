from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from loader import dp, telegram_user_api
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
    await message.answer(user)
    msg = (
        f"👤 <b>Ваш профиль</b>:\n\n"
        f"Имя: {user.get('name', 'NoName')}\n"
        f"Ник: {user.get('nick_name', 'NoName')}\n"
        f"Telegram ID: {user.get('user_id')}\n"
        f"Заблокирован: {'Да' if user.get('is_blocked') else 'Нет'}\n"
        f"Администратор: {'Да' if user.get('is_administrator') else 'Нет'}\n"
        f"Дата регистрации: {user.get('date_join', '—')}"
    )

    await message.answer(msg, parse_mode="HTML")


@dp.message_handler(state=ProfileStates.waiting_email)
async def set_email(message: types.Message, state: FSMContext, user: dict):
    """
    Получаем email от пользователя и привязываем TelegramUser к AppUser через bind_user endpoint.
    """
    email = message.text.strip()

    if "@" not in email:
        await message.answer("Это не похоже на email. Попробуй ещё раз:")
        return

    # Проверяем, что пользователь ещё не привязан
    if user.get("app_user"):
        await message.answer("У вас уже есть привязанный профиль.")
        await state.finish()
        return

    # Вызываем bind_user endpoint
    result = await telegram_user_api.bind_user(id=user["id"], json={"email": email})

    if not result:
        await message.answer("Ошибка при привязке профиля. Попробуй позже.")
        return

    await message.answer(
        f"✅ Профиль успешно создан и привязан!\n\n"
        f"Email: {result['email']}\n"
        f"Пароль: <code>{result['password']}</code>\n\n"
        f"Не забудь сохранить пароль, его нельзя будет посмотреть снова.",
        parse_mode="HTML",
    )

    await state.finish()
