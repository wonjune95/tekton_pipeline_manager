from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/download")
def download(name: str, response: Response):
    # 외부 입력을 응답 헤더에 넣음
    # ruleid: mois-1-13-http-response-splitting-py
    response.headers["X-File-Name"] = name
    return {"ok": True}


@app.get("/track")
def track(campaign: str):
    # ruleid: mois-1-13-http-response-splitting-py
    return JSONResponse({"ok": True}, headers={"X-Campaign": campaign})
