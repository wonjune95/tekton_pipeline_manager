import flask
from fastapi import FastAPI, WebSocket
from flask_restful import Resource
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

app = FastAPI()
last_item = None
last_order = None
last_editor = None
patch_count = 0
deleted_total = 0
last_probe = None
last_origin = None
last_method = None
active_socket = None


@app.get("/items/{item_id}")
def read_item(item_id: int):
    global last_item
    # ruleid: mois-6-01-shared-field-in-singleton-py
    last_item = item_id
    return {"id": item_id}


@app.post("/orders")
def create_order(order: dict):
    global last_order
    # ruleid: mois-6-01-shared-field-in-singleton-py
    last_order = order
    return {"saved": True}


@app.put("/items/{item_id}")
def replace_item(item_id: int, editor: str):
    global last_editor
    # ruleid: mois-6-01-shared-field-in-singleton-py
    last_editor = editor
    return {"id": item_id}


@app.patch("/items/{item_id}")
def patch_item(item_id: int):
    global patch_count
    # ruleid: mois-6-01-shared-field-in-singleton-py
    patch_count += 1
    return {"id": item_id}


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    global deleted_total
    # ruleid: mois-6-01-shared-field-in-singleton-py
    deleted_total += 1
    return {"deleted": item_id}


@app.head("/items/{item_id}")
def probe_item(item_id: int):
    global last_probe
    # ruleid: mois-6-01-shared-field-in-singleton-py
    last_probe = item_id


@app.options("/items")
def item_options(origin: str = ""):
    global last_origin
    # ruleid: mois-6-01-shared-field-in-singleton-py
    last_origin = origin
    return {"allow": "GET, POST"}


@app.api_route("/echo", methods=["GET", "POST"])
def echo(method: str = "GET"):
    global last_method
    # ruleid: mois-6-01-shared-field-in-singleton-py
    last_method = method
    return {"method": method}


@app.websocket("/ws")
async def stream(ws: WebSocket):
    global active_socket
    await ws.accept()
    # ruleid: mois-6-01-shared-field-in-singleton-py
    active_socket = ws


class QueueViewSet(ViewSet):
    waiting = []
    by_user = {}
    online = set()

    def create(self, request):
        # ruleid: mois-6-01-shared-field-in-singleton-py
        self.waiting.insert(0, request.user.pk)
        # ruleid: mois-6-01-shared-field-in-singleton-py
        self.by_user.update({request.user.pk: request.data})
        return Response(status=201)

    def destroy(self, request, pk=None):
        # ruleid: mois-6-01-shared-field-in-singleton-py
        self.waiting.remove(request.user.pk)
        # ruleid: mois-6-01-shared-field-in-singleton-py
        self.by_user.pop(request.user.pk, None)
        # ruleid: mois-6-01-shared-field-in-singleton-py
        self.online.discard(request.user.pk)
        return Response(status=204)

    def list(self, request):
        # ruleid: mois-6-01-shared-field-in-singleton-py
        newest = self.by_user.popitem()
        # ruleid: mois-6-01-shared-field-in-singleton-py
        self.waiting.clear()
        return Response({"newest": newest})


class TokenResource(Resource):
    issued = {}
    last_token = None

    def post(self):
        token = flask.request.headers.get("X-Token", "")
        # ruleid: mois-6-01-shared-field-in-singleton-py
        self.issued[token] = flask.request.remote_addr
        # ruleid: mois-6-01-shared-field-in-singleton-py
        TokenResource.last_token = token
        return {"issued": len(self.issued)}
