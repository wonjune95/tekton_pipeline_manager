"""공통 source 블록(외부 입력으로 보는 것)을 끝까지 확인하는 예제. 모든 *-py taint 규칙이 같은 블록을 쓴다."""
import os
from typing import Annotated

import flask
from fastapi import FastAPI, Query
from flask import Flask
from pydantic import BaseModel
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

api = FastAPI()
web = Flask(__name__)


class ItemCreate(BaseModel):
    name: str
    tag: str


@api.post("/items")
def create_item(item: ItemCreate):
    # 요청 본문 모델의 필드
    # ruleid: mois-1-05-os-command-injection-py
    os.system("touch /srv/items/" + item.name)
    return {"ok": True}


@api.get("/items/search")
def search_items(q: Annotated[str, Query(max_length=10)]):
    # Annotated[str, Query(...)] 질의 매개변수 (길이 제한은 내용 검증이 아니다)
    # ruleid: mois-1-05-os-command-injection-py
    os.system(f"grep -r {q} /srv/items")
    return {"ok": True}


@web.route("/logs/<name>")
def show_log(name):
    # Flask 경로 매개변수 (타입 표기 없음)
    # ruleid: mois-1-05-os-command-injection-py
    out = os.popen("tail -n 50 /var/log/app/" + name).read()
    return {"out": out}


@web.route("/uptime")
def uptime():
    # `import flask` 뒤 flask.request 로 쓰는 형태
    # ruleid: mois-1-05-os-command-injection-py
    out = os.popen("uptime " + flask.request.args["opts"]).read()
    return {"out": out}


def django_view(request):
    # Django request.GET
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + request.GET["host"])
    # Django request.POST / request.COOKIES / request.META
    # ruleid: mois-1-05-os-command-injection-py
    os.system("echo " + request.POST.get("msg", ""))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("echo " + request.COOKIES["lang"])
    # ruleid: mois-1-05-os-command-injection-py
    os.system("echo " + request.META.get("HTTP_USER_AGENT", ""))


class LogSearchView(ListAPIView):
    def list(self, request, *args, **kwargs):
        # DRF self.request.query_params
        keyword = self.request.query_params.get("keyword", "")
        # ruleid: mois-1-05-os-command-injection-py
        out = os.popen("grep " + keyword + " /var/log/app/app.log").read()
        # DRF request.data
        # ruleid: mois-1-05-os-command-injection-py
        os.system("logger " + request.data["message"])
        return Response({"out": out})
