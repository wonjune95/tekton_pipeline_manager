import sys
import traceback

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from flask import Flask, jsonify
from starlette.applications import Starlette

from .services import load_order, save_order

# ruleid: mois-4-01-error-message-exposure-py
asgi = Starlette(debug=True)
api = FastAPI()
web = Flask(__name__)
# ruleid: mois-4-01-error-message-exposure-py
web.debug = True
# ruleid: mois-4-01-error-message-exposure-py
web.config["DEBUG"] = True


@api.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    # FastAPI 예외 처리기가 예외 내용을 그대로 돌려준다
    # ruleid: mois-4-01-error-message-exposure-py
    return JSONResponse({"detail": str(exc)}, status_code=400)


@web.route("/orders/<int:order_id>/debug")
def order_debug(order_id):
    try:
        return load_order(order_id)
    except Exception:
        exc_type, exc_value, tb = sys.exc_info()
        # ruleid: mois-4-01-error-message-exposure-py
        traceback.print_exception(exc_type, exc_value, tb)
        # ruleid: mois-4-01-error-message-exposure-py
        traceback.print_stack()
        # 트레이스백 문자열을 본문으로 돌려준다
        # ruleid: mois-4-01-error-message-exposure-py
        return traceback.format_exc(), 500


@web.route("/orders/<int:order_id>/json")
def order_json(order_id):
    try:
        return load_order(order_id)
    except Exception:
        # ruleid: mois-4-01-error-message-exposure-py
        return jsonify(error="조회 실패", trace=traceback.format_exc())


def save(order):
    try:
        save_order(order)
    except ValueError as exc:
        # ruleid: mois-4-01-error-message-exposure-py
        return repr(exc)
    else:
        return "saved"


def save_many(orders):
    try:
        for order in orders:
            save_order(order)
    except OSError as exc:
        # ruleid: mois-4-01-error-message-exposure-py
        return {"error": exc.args}
    else:
        return {"saved": len(orders)}
    finally:
        orders.clear()
