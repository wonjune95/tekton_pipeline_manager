from fastapi import FastAPI

app = FastAPI()


@app.get("/label")
def label(text: str, width: int = 10):
    # ok: mois-1-17-format-string-py 형식은 상수, 입력은 인자
    return {"label": "%-*s|" % (width, text)}
