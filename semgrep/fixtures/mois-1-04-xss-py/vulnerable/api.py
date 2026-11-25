from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/welcome")
def welcome(name: str):
    # 외부 입력을 이스케이프 없이 HTML 응답에 출력
    # ruleid: mois-1-04-xss-py
    return HTMLResponse(content="<h1>Welcome " + name + "</h1>")


@app.get("/banner", response_class=HTMLResponse)
def banner(text: str):
    # ruleid: mois-1-04-xss-py
    return f"<div class='banner'>{text}</div>"
