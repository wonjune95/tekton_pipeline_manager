import urllib.request

import httpx
from fastapi import FastAPI

app = FastAPI()


@app.get("/proxy")
async def proxy(target: str):
    async with httpx.AsyncClient(timeout=5) as client:
        # 외부 입력 URL 로 요청
        # ruleid: mois-1-12-ssrf-py
        resp = await client.get(target)
    return {"status": resp.status_code}


@app.get("/avatar")
def avatar(host: str, user_id: str):
    # 호스트를 외부 입력으로 정함
    # ruleid: mois-1-12-ssrf-py
    with urllib.request.urlopen(f"https://{host}/avatars/{user_id}.png", timeout=5) as resp:
        return {"size": len(resp.read())}
