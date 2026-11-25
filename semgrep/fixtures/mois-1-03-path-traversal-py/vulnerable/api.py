from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()
REPORT_DIR = Path("/srv/reports")


@app.get("/reports/{name}")
def get_report(name: str):
    # 경로 매개변수를 검증 없이 기준 디렉터리에 붙임
    # ruleid: mois-1-03-path-traversal-py
    return FileResponse(REPORT_DIR / name)


@app.get("/notes")
def read_note(title: str):
    # pathlib 로 만든 경로도 같음
    # ruleid: mois-1-03-path-traversal-py
    return {"body": (REPORT_DIR / "notes" / title).read_text(encoding="utf-8")}
