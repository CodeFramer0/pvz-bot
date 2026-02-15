import logging

import aiohttp

logger = logging.getLogger("BaseAPI")


class BaseAPI:
    BASE_URL = "http://web:8000/api/v1/"

    _session: aiohttp.ClientSession | None = None

    def __init__(self, endpoint: str, jwt_client):
        self.endpoint = self.BASE_URL + endpoint
        self.jwt_client = jwt_client

    @classmethod
    async def get_session(cls) -> aiohttp.ClientSession:
        if cls._session is None or cls._session.closed:
            timeout = aiohttp.ClientTimeout(total=30)
            cls._session = aiohttp.ClientSession(timeout=timeout)
        return cls._session

    async def _headers(self):
        try:
            token = await self.jwt_client.get_access()
        except Exception:
            await self.jwt_client._login()
            token = await self.jwt_client.get_access()

        return {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    @staticmethod
    async def _process_response(response: aiohttp.ClientResponse) -> dict | None:
        try:
            data = await response.json()
            response.raise_for_status()
            if isinstance(data, list):
                return data[0] if len(data) == 1 else data
            return data
        except Exception as e:
            logger.error(f"API error: {e}")
            try:
                logger.error(await response.text())
            except Exception:
                pass
            return None

    def _build_url(self, path: str = "", id: int | None = None) -> str:
        if id is not None:
            return f"{self.endpoint}{id}/"
        if path:
            return f"{self.endpoint}{path}"
        return self.endpoint

    async def get(self, params=None, id: int | None = None, path: str = ""):
        url = self._build_url(path=path, id=id)
        session = await self.get_session()
        async with session.get(
            url, params=params, headers=await self._headers()
        ) as resp:
            return await self._process_response(resp)

    async def post(self, path: str = "", json: dict | None = None):
        url = self._build_url(path=path)
        session = await self.get_session()
        async with session.post(url, json=json, headers=await self._headers()) as resp:
            return await self._process_response(resp)

    async def put(self, id: int, json: dict | None = None):
        url = self._build_url(id=id)
        session = await self.get_session()
        async with session.put(url, json=json, headers=await self._headers()) as resp:
            return await self._process_response(resp)

    async def patch(self, id: int, json: dict | None = None):
        url = self._build_url(id=id)
        session = await self.get_session()
        async with session.patch(url, json=json, headers=await self._headers()) as resp:
            return await self._process_response(resp)

    async def delete(self, id: int):
        url = self._build_url(id=id)
        session = await self.get_session()
        async with session.delete(url, headers=await self._headers()) as resp:
            return await self._process_response(resp)

    @classmethod
    async def close_session(cls):
        if cls._session and not cls._session.closed:
            await cls._session.close()
