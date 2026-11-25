import aiohttp


# aiohttp 세션의 요청 메서드마다 ssl=False 로 인증서 검증을 끌 수 있다
class DeviceGateway:
    def __init__(self, session: aiohttp.ClientSession, base_url):
        self.session = session
        self.base_url = base_url

    async def replace(self, device_id, body):
        # ruleid: mois-2-11-improper-cert-validation-py
        async with self.session.put(f"{self.base_url}/devices/{device_id}", json=body, ssl=False) as resp:
            return await resp.json()

    async def rename(self, device_id, name):
        # ruleid: mois-2-11-improper-cert-validation-py
        async with self.session.patch(f"{self.base_url}/devices/{device_id}", json={"name": name}, ssl=False) as resp:
            return resp.status

    async def remove(self, device_id):
        # ruleid: mois-2-11-improper-cert-validation-py
        async with self.session.delete(f"{self.base_url}/devices/{device_id}", ssl=False) as resp:
            return resp.status

    async def exists(self, device_id):
        # ruleid: mois-2-11-improper-cert-validation-py
        async with self.session.head(f"{self.base_url}/devices/{device_id}", ssl=False) as resp:
            return resp.status == 200

    async def allowed_methods(self):
        # ruleid: mois-2-11-improper-cert-validation-py
        async with self.session.options(f"{self.base_url}/devices", ssl=False) as resp:
            return resp.headers.get("Allow", "")

    async def call(self, method, path, **kwargs):
        # ruleid: mois-2-11-improper-cert-validation-py
        async with self.session.request(method, self.base_url + path, ssl=False, **kwargs) as resp:
            return await resp.json()

    async def events(self):
        # ruleid: mois-2-11-improper-cert-validation-py
        async with self.session.ws_connect(self.base_url + "/events", ssl=False) as ws:
            async for message in ws:
                yield message
