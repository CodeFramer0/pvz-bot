from aiogram import executor
from api.base import BaseAPI
from handlers import *
from loader import dp
from middlewares import *
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)


async def on_shutdown(dp):
    await BaseAPI.close_session()


executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
executor.start_polling(dp, on_shutdown=on_shutdown)
