from fastapi import FastAPI

app = FastAPI()


@app.get("/label")
def label(pattern: str, width: int = 10):
    # 외부 입력을 % 형식 문자열로 사용
    # ruleid: mois-1-17-format-string-py
    return {"label": pattern % width}
