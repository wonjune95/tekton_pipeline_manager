import urllib.request
from urllib.parse import quote

import httpx
from fastapi import FastAPI

app = FastAPI()


@app.get("/proxy")
async def proxy(item_id: str):
    async with httpx.AsyncClient(timeout=5) as client:
        # ok: mois-1-12-ssrf-py 스킴·호스트는 고정하고 입력은 경로에만 사용
        resp = await client.get(f"https://api.example.go.kr/v1/items/{quote(item_id, safe='')}")
    return {"status": resp.status_code}


@app.get("/avatar")
def avatar(user_id: str):
    # ok: mois-1-12-ssrf-py
    with urllib.request.urlopen(f"https://static.example.go.kr/avatars/{quote(user_id, safe='')}.png", timeout=5) as resp:
        return {"size": len(resp.read())}
