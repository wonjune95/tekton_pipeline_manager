from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

app = FastAPI()
REDIRECT_TARGETS = {"docs": "/docs/index.html", "status": "/status"}


@app.get("/go")
def go(target: str):
    url = REDIRECT_TARGETS.get(target)
    if url is None:
        raise HTTPException(status_code=404, detail="unknown target")
    return RedirectResponse(url=url)


@app.get("/board/{board_id}/back")
def back(board_id: str):
    # ok: mois-1-07-open-redirect-py 고정된 상대 경로 뒤에만 입력을 붙임
    return RedirectResponse(f"/board/{board_id}")
