from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from api.endpoints import (AuthAPI, MarketplaceAPI, OrderAPI, PickupPointAPI,
                           TelegramUserAPI, UsersAPI)
from config import BOT_TOKEN
from services.jwt_client import JWTClient

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = RedisStorage2("redis", 6379, db=5)
dp = Dispatcher(bot, storage=storage)
jwt_client = JWTClient()

auth_api = AuthAPI(jwt_client)
users_api = UsersAPI(jwt_client)
telegram_user_api = TelegramUserAPI(jwt_client)
pickup_point_api = PickupPointAPI(jwt_client)
order_api = OrderAPI(jwt_client)
marketplace_api = MarketplaceAPI(jwt_client)
