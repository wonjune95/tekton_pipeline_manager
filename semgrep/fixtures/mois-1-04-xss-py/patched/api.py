import html

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/welcome")
def welcome(name: str):
    # ok: mois-1-04-xss-py html.escape 로 이스케이프
    return HTMLResponse(content="<h1>Welcome " + html.escape(name) + "</h1>")


@app.get("/banner", response_class=HTMLResponse)
def banner(text: str):
    # ok: mois-1-04-xss-py
    return f"<div class='banner'>{html.escape(text)}</div>"


@app.get("/echo")
def echo(name: str):
    # ok: mois-1-04-xss-py FastAPI 는 문자열 반환값을 JSON(application/json)으로 응답한다
    return name


@app.get("/hello")
def hello(name: str):
    # ok: mois-1-04-xss-py
    return "Hello " + name
