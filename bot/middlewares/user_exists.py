import logging

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from api import TelegramUserAPI


class UserExistsMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()
        self.api = TelegramUserAPI()

    async def on_pre_process_message(self, message: types.Message, data: dict):
        user_id = message.from_user.id
        user = await self.api.get(params={"user_id": user_id})
        nick_name = message.from_user.username

        if not nick_name:
            nick_name = "NoName"

        if not user:
            user = await self.api.create(
                body={
                    "name": message.from_user.full_name,
                    "nick_name": nick_name,
                    "user_id": user_id,
                }
            )

            data["user"] = user
            return

        user = await self.api.update(
            id=user["id"],
            body={
                "user_id": message.from_user.id,
                "name": nick_name,
                "nick_name": nick_name,
            },
        )

        data["user"] = user
        return

    async def on_pre_process_callback_query(
        self, callback_query: types.CallbackQuery, data: dict
    ):
        user_id = callback_query.from_user.id
        user = await self.api.get(params={"user_id": user_id})

        nick_name = callback_query.from_user.username

        if not nick_name:
            nick_name = "NoName"

        if not user:
            user = await self.api.create(
                body={
                    "name": f"{callback_query.from_user.full_name}",
                    "nick_name": nick_name,
                    "chat_id": user_id,
                }
            )

        data["user"] = user
