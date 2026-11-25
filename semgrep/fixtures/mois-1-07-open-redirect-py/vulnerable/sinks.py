import starlette.responses
from django.http import HttpResponse, HttpResponsePermanentRedirect
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from flask import Flask, redirect, request

app = Flask(__name__)
api = FastAPI()


@app.route("/out")
def out():
    # Flask redirect
    # ruleid: mois-1-07-open-redirect-py
    return redirect(request.args["url"])


def moved(request):
    # ruleid: mois-1-07-open-redirect-py
    return HttpResponsePermanentRedirect(request.GET.get("to", "/"))


def location_header(request):
    target = request.GET.get("to", "/")
    response = HttpResponse(status=302)
    # Location 헤더를 직접 넣음
    # ruleid: mois-1-07-open-redirect-py
    response["Location"] = target
    # ruleid: mois-1-07-open-redirect-py
    response.headers["Location"] = target
    return response


@api.get("/jump")
def jump(to: str, back: str):
    # ruleid: mois-1-07-open-redirect-py
    first = RedirectResponse(to, status_code=303)
    # ruleid: mois-1-07-open-redirect-py
    second = starlette.responses.RedirectResponse(back)
    # ruleid: mois-1-07-open-redirect-py
    third = starlette.responses.RedirectResponse(url=back, status_code=307)
    return first or second or third
