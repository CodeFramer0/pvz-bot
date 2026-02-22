import logging
import os
import aiohttp
from .jwt_storage import save_bot_tokens, get_bot_tokens

# Сверяем с настройками твоего Django
API_BASE_URL = os.getenv("API_BASE_URL", "http://web:8000/api/v1/")
BOT_LOGIN = os.getenv("BOT_LOGIN")      # Твой email/username из Django
BOT_PASSWORD = os.getenv("BOT_PASSWORD") # Твой пароль

logger = logging.getLogger("JWTClient")

class JWTClient:
    def __init__(self):
        self.base_url = API_BASE_URL.rstrip('/') + '/'

    async def get_access(self):
        """Основной метод: вернет живой токен, чего бы это ни стоило"""
        tokens = get_bot_tokens()
        access = tokens.get("access")
        refresh = tokens.get("refresh")

        # 1. Если вообще нет токенов — логинимся
        if not access:
            return await self._login()

        # 2. Проверяем, живой ли access (делаем легкий запрос)
        if not await self._is_token_valid(access):
            logger.info("Access token expired, trying to refresh...")
            # 3. Пробуем рефреш
            new_access = await self._refresh_token(refresh)
            if new_access:
                return new_access
            else:
                # 4. Если рефреш сдох — полный перелогин
                logger.info("Refresh failed, performing full login...")
                return await self._login()
        
        return access

    async def _is_token_valid(self, token):
        """Проверка токена через эндпоинт /me/"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}users/me/",
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=5
                ) as resp:
                    return resp.status == 200
        except Exception:
            return False

    async def _login(self):
        """Логин: используем эндпоинт /auth/login/ и ключ 'username'"""
        async with aiohttp.ClientSession() as session:
            payload = {"username": BOT_LOGIN, "password": BOT_PASSWORD}
            async with session.post(f"{self.base_url}auth/login/", json=payload) as resp:
                if resp.status != 200:
                    logger.error(f"Login failed: {await resp.text()}")
                    return None
                
                data = await resp.json()
                save_bot_tokens(data["access"], data["refresh"])
                logger.info("New JWT session created and saved to Redis")
                return data["access"]

    async def _refresh_token(self, refresh):
        """Обновление через /auth/refresh/"""
        if not refresh:
            return None
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{self.base_url}auth/refresh/",
                    json={"refresh": refresh}
                ) as resp:
                    if resp.status != 200:
                        return None
                    data = await resp.json()
                    # Сохраняем новый access. Если прилетел новый refresh — его тоже.
                    new_refresh = data.get("refresh", refresh)
                    save_bot_tokens(data["access"], new_refresh)
                    return data["access"]
            except Exception as e:
                logger.info(f"Refresh error: {e}")
                return None
