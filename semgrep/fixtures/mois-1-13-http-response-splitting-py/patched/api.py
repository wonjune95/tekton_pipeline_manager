from urllib.parse import quote

from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/download")
def download(name: str, response: Response):
    # ok: mois-1-13-http-response-splitting-py 개행 문자를 제거한 뒤 헤더에 넣음
    response.headers["X-File-Name"] = name.replace("\r", "").replace("\n", "")
    return {"ok": True}


@app.get("/track")
def track(campaign: str):
    # ok: mois-1-13-http-response-splitting-py URL 인코딩한 값
    return JSONResponse({"ok": True}, headers={"X-Campaign": quote(campaign)})
