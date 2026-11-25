from fastapi import FastAPI
from jinja2 import Environment, select_autoescape

app = FastAPI()
ENV = Environment(autoescape=select_autoescape(default=True))
PREVIEW = ENV.from_string("<article>{{ body }}</article>")


@app.post("/preview")
def preview(body: str):
    # ok: mois-1-02-code-injection-py 템플릿은 고정하고 입력은 변수로 전달
    return {"html": PREVIEW.render(body=body)}
