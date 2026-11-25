import os
import socket
import sys

from django.http import HttpRequest, HttpResponse
from flask import Flask
from flask.views import MethodView
from rest_framework.response import Response
from rest_framework.views import APIView

app = Flask(__name__)


def stop_worker(request: HttpRequest):
    # 타입 표기가 있는 Django 뷰
    # ruleid: mois-7-02-dangerous-api-py
    os.abort()


class MaintenanceView(APIView):
    def post(self, request):
        # ruleid: mois-7-02-dangerous-api-py
        assert request.user.is_superuser
        # ruleid: mois-7-02-dangerous-api-py
        assert request.user.has_perm("ops.restart"), "권한 없음"
        # ruleid: mois-7-02-dangerous-api-py
        exit(0)

    def delete(self, request):
        # ruleid: mois-7-02-dangerous-api-py
        quit()


class RelayAPI(MethodView):
    def get(self):
        # 요청 인자가 없는 뷰 클래스 메서드
        # ruleid: mois-7-02-dangerous-api-py
        conn = socket.create_connection(("relay.internal", 7000), timeout=3)
        conn.close()
        return "ok"


@app.route("/listen")
def listen():
    # ruleid: mois-7-02-dangerous-api-py
    server = socket.create_server(("0.0.0.0", 9100))
    server.close()
    return "ok"


def check_login(user, password):
    # 뷰 밖에서도 assert 로 하는 인증 검사는 -O 에서 사라진다
    # ruleid: mois-7-02-dangerous-api-py
    assert user.check_password(password)
    # ruleid: mois-7-02-dangerous-api-py
    assert user.is_active, "inactive"
    return True
