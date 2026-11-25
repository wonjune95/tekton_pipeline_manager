"""이름만으로는 의존성이라고 증명되지 않는 매개변수 — 요청 본문 모델일 수 있어 외부 입력으로 본다."""
import subprocess

from fastapi import FastAPI

from .services import ItemService

app = FastAPI()


@app.post("/items/reindex")
def reindex(svc: ItemService):
    # Depends 가 없으면 FastAPI 는 이 매개변수를 요청 본문에서 만든다 (…Service 라는 이름은 증명이 아니다)
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run("reindex --index " + svc.index_name, shell=True, check=False)
    return {"ok": True}
