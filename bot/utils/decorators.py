import datetime
import functools
import logging
import traceback

import api
from loader import bot


def error_handler():
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            try:
                f = await func(*args, **kwargs)
            except Exception:
                await bot.send_message(
                    chat_id=args[0]["from"]["id"],
                    text="Произошла ошибка, мы уже работаем над ее исправлением, а пока возвращаем вас в исходное меню.",
                    reply_markup=bot_start_keyboard(),
                )
                # return logging.error(traceback.print_exc())

        return wrapped

    return wrapper
