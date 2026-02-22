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

        # 1. Получаем ответ от API (это будет список [ {...} ])
        response = await self.api.get(params={"user_id": user_id})

        # 2. Извлекаем юзера, если список не пуст
        user = response[0] if isinstance(response, list) and len(response) > 0 else None

        if not user:
            # создаём нового
            return await self.api.post(
                json={
                    "name": full_name,
                    "nick_name": nick_name,
                    "user_id": user_id,
                }
            )

        # 3. Теперь 'user' точно словарь, и эта проверка сработает
        need_update = (
            user.get("name") != full_name or user.get("nick_name") != nick_name
        )
        
        if need_update:
            return await self.api.patch(
                id=user["id"],
                json={
                    "name": full_name,
                    "nick_name": nick_name,
                },
            )

        return user

    async def on_pre_process_message(self, message, data: dict):
        data["user"] = await self._get_or_create_or_update(message.from_user)

    async def on_pre_process_callback_query(self, callback_query, data: dict):
        data["user"] = await self._get_or_create_or_update(callback_query.from_user)
