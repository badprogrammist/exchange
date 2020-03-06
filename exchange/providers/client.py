import aiohttp


class ClientError(Exception):
    pass


class HttpClient:

    @classmethod
    def create(cls):
        session = aiohttp.ClientSession()
        return cls(session)

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def _get_json(self, endpoint: str, params: dict) -> dict:
        async with self.session.get(endpoint, params=params) as response:
            return await response.json()

    async def get_json(self, endpoint: str, params: dict) -> dict:
        try:
            return await self._get_json(endpoint, params)
        except aiohttp.ClientError as err:
            raise ClientError("Could not get data") from err

    async def release_resources(self):
        if self.session and not self.session.closed:
            await self.session.close()
