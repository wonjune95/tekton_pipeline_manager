"""정수형으로 선언한 핸들러 매개변수 — 라우트 데코레이터 종류마다 한 줄."""
import os

from fastapi import APIRouter, WebSocket
from flask import Flask

router = APIRouter()
flask_app = Flask(__name__)


@router.put("/buffers/{buffer_id}")
def resize_buffer(buffer_id: str, size: int):
    # ruleid: mois-1-14-integer-overflow-py
    return {"id": buffer_id, "size": len(bytearray(size))}


@router.patch("/buffers/{buffer_id}")
def grow_buffer(buffer_id: str, extra: int):
    # ruleid: mois-1-14-integer-overflow-py
    return {"id": buffer_id, "grown": len(bytearray(extra))}


@router.delete("/buffers/{buffer_id}")
def wipe_buffer(buffer_id: str, length: int):
    # 지운 자리를 0 으로 덮어쓴다
    # ruleid: mois-1-14-integer-overflow-py
    return {"id": buffer_id, "wiped": len(bytearray(length))}


@router.head("/random/{length}")
def random_head(length: int):
    # ruleid: mois-1-14-integer-overflow-py
    os.urandom(length)
    return None


@router.options("/random/{length}")
def random_options(length: int):
    # ruleid: mois-1-14-integer-overflow-py
    return {"sample": os.urandom(length).hex()}


@router.api_route("/padding", methods=["GET", "POST"])
def padding(width: int):
    # ruleid: mois-1-14-integer-overflow-py
    return {"pad": " " * width}


@router.websocket("/ws/noise/{chunk}")
async def noise(websocket: WebSocket, chunk: int):
    await websocket.accept()
    # ruleid: mois-1-14-integer-overflow-py
    await websocket.send_bytes(os.urandom(chunk))


@flask_app.route("/blank/<int:lines>")
def blank(lines: int):
    # ruleid: mois-1-14-integer-overflow-py
    return "\n" * lines
