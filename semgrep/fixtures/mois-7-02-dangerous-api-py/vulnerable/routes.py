import os
import socket
import sys

from django.contrib import admin
from fastapi import FastAPI, WebSocket
from flask_restful import Resource
from rest_framework.viewsets import ViewSet

app = FastAPI()


@app.get("/admin/stop")
def stop():
    # ruleid: mois-7-02-dangerous-api-py
    sys.exit(0)


@app.put("/admin/mode")
def set_mode(mode: str):
    if mode == "off":
        # ruleid: mois-7-02-dangerous-api-py
        os._exit(1)
    return {"mode": mode}


@app.patch("/admin/workers/{worker_id}")
def pause_worker(worker_id: int):
    # ruleid: mois-7-02-dangerous-api-py
    conn = socket.create_connection(("worker.internal", 7100 + worker_id), timeout=3)
    conn.sendall(b"pause")
    conn.close()
    return {"paused": worker_id}


@app.delete("/admin/workers/{worker_id}")
def kill_worker(worker_id: int):
    # ruleid: mois-7-02-dangerous-api-py
    os.abort()


@app.head("/admin/ping")
def ping():
    # ruleid: mois-7-02-dangerous-api-py
    socket.create_connection(("db.internal", 5432), timeout=1).close()


@app.options("/admin/relay")
def relay_options():
    # ruleid: mois-7-02-dangerous-api-py
    probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    probe.close()
    return {"allow": "GET, POST"}


@app.api_route("/admin/relay", methods=["GET", "POST"])
def relay():
    # ruleid: mois-7-02-dangerous-api-py
    upstream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    upstream.connect(("relay.internal", 7000))
    upstream.close()
    return {"relayed": True}


@app.websocket("/ws/relay")
async def relay_ws(ws: WebSocket):
    await ws.accept()
    # ruleid: mois-7-02-dangerous-api-py
    server = socket.create_server(("0.0.0.0", 9200))
    server.close()


class WorkerViewSet(ViewSet):
    def get_queryset(self):
        if not os.path.isdir("/var/app/workers"):
            # 뷰셋의 보조 메서드도 요청 처리 중에 실행된다
            # ruleid: mois-7-02-dangerous-api-py
            sys.exit(3)
        return os.listdir("/var/app/workers")


class ShutdownResource(Resource):
    def post(self):
        # ruleid: mois-7-02-dangerous-api-py
        os._exit(0)


class ReportAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        # 뷰 클래스가 아니어도 (self, request) 를 받는 메서드는 요청 처리 코드다
        # ruleid: mois-7-02-dangerous-api-py
        relay = socket.create_connection(("audit.internal", 9000), timeout=3)
        relay.close()
        return super().changelist_view(request, extra_context)


def check_member(user, perms):
    # ruleid: mois-7-02-dangerous-api-py
    assert user.is_authenticated
    # ruleid: mois-7-02-dangerous-api-py
    assert user.is_admin, "admin only"
    # ruleid: mois-7-02-dangerous-api-py
    assert user.has_perms(perms)
    return True
