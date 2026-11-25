from fastapi import FastAPI
from jinja2 import Template

app = FastAPI()


@app.post("/preview")
def preview(body: str):
    # 외부 입력을 Jinja2 템플릿 원문으로 사용 (SSTI)
    # ruleid: mois-1-02-code-injection-py
    return {"html": Template(body).render()}
