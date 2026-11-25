from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()
REPORT_DIR = Path("/srv/reports")


@app.get("/reports/{name}")
def get_report(name: str):
    target = (REPORT_DIR / name).resolve()
    # 정규화한 경로가 기준 디렉터리 안인지 확인
    if not target.is_relative_to(REPORT_DIR):
        raise HTTPException(status_code=404, detail="not found")
    # ok: mois-1-03-path-traversal-py 기준 디렉터리 밖이면 위에서 예외
    return FileResponse(target)


@app.get("/notes")
def read_note(title: str):
    # ok: mois-1-03-path-traversal-py 파일명만 남김
    path = REPORT_DIR / "notes" / Path(title).name
    return {"body": path.read_text(encoding="utf-8")}
