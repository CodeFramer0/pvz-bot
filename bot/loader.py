from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from api import OrderAPI, PickupPointAPI, TelegramUserAPI
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = RedisStorage2("redis", 6379, db=5)
dp = Dispatcher(bot, storage=storage)

telegram_user_api = TelegramUserAPI()
pickup_point_api = PickupPointAPI()
order_api = OrderAPI()
