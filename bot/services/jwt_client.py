# bot/services/jwt_client.py
import logging
import os

import aiohttp

API_BASE_URL = os.getenv("API_BASE_URL", "http://web:8000/api/v1/")
BOT_LOGIN = os.getenv("BOT_LOGIN")
BOT_PASSWORD = os.getenv("BOT_PASSWORD")

logger = logging.getLogger("JWTClient")


class JWTClient:
    def __init__(self):
        self._access = None
        self._refresh = None

    async def _login(self):
        """Стандартный логин, получаем access + refresh"""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                API_BASE_URL + "auth/login/email/",
                json={"email": BOT_LOGIN, "password": BOT_PASSWORD},
            ) as resp:
                resp.raise_for_status()
                data = await resp.json()
                self._access = data["access"]
                self._refresh = data["refresh"]
                logger.info("JWT login success, tokens updated")

    async def _refresh_token(self):
        """Пробуем обновить access через refresh токен"""
        if not self._refresh:
            return False
        async with aiohttp.ClientSession() as session:
            async with session.post(
                API_BASE_URL + "auth/token/refresh/",
                json={"refresh": self._refresh},
            ) as resp:
                if resp.status != 200:
                    return False
                data = await resp.json()
                self._access = data["access"]
                logger.info("JWT refresh success, access token updated")
                return True

    async def get_access(self):
        """Получаем актуальный access токен"""
        if not self._access:
            await self._login()
        # Пробуем доступ к API для проверки (optional)
        return self._access

    async def invalidate(self):
        """Очистить токены"""
        self._access = None
        self._refresh = None
