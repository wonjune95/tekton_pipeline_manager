import logging
import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from flask import Flask
from starlette.applications import Starlette

from .services import save_order

logger = logging.getLogger(__name__)
# ok: mois-4-01-error-message-exposure-py 디버그 모드를 켜지 않는다
asgi = Starlette()
api = FastAPI()
web = Flask(__name__)
# ok: mois-4-01-error-message-exposure-py 상수 True 가 아니라 환경에서 읽는다
web.debug = os.environ.get("FLASK_DEBUG") == "1"


@api.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    # ok: mois-4-01-error-message-exposure-py 상세 내용은 로그로, 응답은 정해진 코드
    logger.warning("bad request: %s", exc)
    return JSONResponse({"detail": "E400"}, status_code=400)


def save(order):
    try:
        save_order(order)
    except ValueError as exc:
        # ok: mois-4-01-error-message-exposure-py 트레이스백은 로그로만 남긴다
        logger.error("save failed: %s", exc, exc_info=True)
        return "E400"
    else:
        return "saved"
