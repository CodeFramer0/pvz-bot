import aiohttp
import logging
import time
from services.jwt_client import JWTClient

RESET = "\033[0m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"

logger = logging.getLogger("BaseAPI")


class BaseAPI:
    BASE_URL = "http://web:8000/api/v1/"

    def __init__(self, endpoint: str, jwt_client: JWTClient):
        self.endpoint = self.BASE_URL + endpoint
        self.jwt_client = jwt_client

    async def _headers(self):
        """
        Проверяем токен и делаем логин при необходимости.
        """
        try:
            token = await self.jwt_client.get_access()
        except Exception as e:
            logger.warning(f"JWT expired or missing, re-login: {e}")
            await self.jwt_client._login()
            token = await self.jwt_client.get_access()

        return {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }

    @staticmethod
    async def _process_response(response: aiohttp.ClientResponse) -> dict | None:
        """
        Process the API response.

        Args:
            response (aiohttp.ClientResponse): The API response object.

        Returns:
            dict | None: Parsed JSON data from the response or None if an error occurs.
        """
        try:
            data = await response.json()
            response.raise_for_status()
            if isinstance(data, list):
                data = data if len(data) > 1 else data[0] if data else None
            return data
        except (aiohttp.ClientError, ValueError) as e:
            logging.error(f"An error occurred during response processing: {e}")
            logging.error(f"Response status: {response.status}")
            logging.error(f"Response content: {await response.text()}")
            return None

    async def get(self, params=None, id: int | None = None):
        url = f"{self.endpoint}{id}/" if id else self.endpoint
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=await self._headers()) as resp:
                return await self._process_response(resp)

    async def post(self, data=None, json=None):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.endpoint, data=data, json=json, headers=await self._headers()) as resp:
                return await self._process_response(resp)

    async def put(self, id: int, data=None, json=None):
        url = f"{self.endpoint}{id}/"
        async with aiohttp.ClientSession() as session:
            async with session.put(url, data=data, json=json, headers=await self._headers()) as resp:
                return await self._process_response(resp)

    async def patch(self, id: int, data=None, json=None):
        url = f"{self.endpoint}{id}/"
        async with aiohttp.ClientSession() as session:
            async with session.patch(url, data=data, json=json, headers=await self._headers()) as resp:
                return await self._process_response(resp)

    async def delete(self, id: int):
        url = f"{self.endpoint}{id}/"
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=await self._headers()) as resp:
                return await self._process_response(resp)
