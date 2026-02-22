from aiogram.dispatcher.middlewares import BaseMiddleware
from api.endpoints import TelegramUserAPI
from loader import jwt_client


class EnsureUserMiddleware(BaseMiddleware):
    def __init__(self):
        """
        :param storage: RedisStorage2
        :param user_ttl_days: Если задано, пользователи будут удаляться из Redis после указанного кол-ва дней
        """
        super().__init__()
        self.api = TelegramUserAPI(jwt_client)

    async def _get_or_create_or_update(self, tg_user):
        user_id = str(tg_user.id)
        nick_name = tg_user.username or "NoName"
        full_name = tg_user.full_name or "NoName"

        return await self.api.post(
            json={
                "user_id": user_id,
                "name": full_name,
                "nick_name": nick_name,
            }
    )

    async def on_pre_process_message(self, message, data: dict):
        data["user"] = await self._get_or_create_or_update(message.from_user)

    async def on_pre_process_callback_query(self, callback_query, data: dict):
        data["user"] = await self._get_or_create_or_update(callback_query.from_user)
