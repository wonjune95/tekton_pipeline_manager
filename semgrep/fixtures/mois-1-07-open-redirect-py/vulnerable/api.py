from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/go")
def go(target: str):
    # 외부 입력 URL 로 리다이렉트
    # ruleid: mois-1-07-open-redirect-py
    return RedirectResponse(url=target)


@app.get("/board/{board_id}/back")
def back(board_id: str, base: str):
    # ruleid: mois-1-07-open-redirect-py
    return RedirectResponse(f"{base}/board/{board_id}")
