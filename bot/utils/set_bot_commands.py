from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Начальное меню"),
            types.BotCommand("cancel", "Отменить создание заказа"),
        ]
    )
