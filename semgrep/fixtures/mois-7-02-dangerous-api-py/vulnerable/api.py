import os

from fastapi import FastAPI

app = FastAPI()


@app.post("/admin/shutdown")
def shutdown():
    # ruleid: mois-7-02-dangerous-api-py
    os._exit(0)  # 라우트 함수에서 프로세스 강제 종료
