from fastapi import FastAPI, HTTPException
from flask import Flask

from .services import load_order

# ruleid: mois-4-01-error-message-exposure-py
api = FastAPI(debug=True)  # 디버그 모드
web = Flask(__name__)


@api.get("/orders/{order_id}")
def order(order_id: int):
    try:
        return load_order(order_id)
    except KeyError as exc:
        # ruleid: mois-4-01-error-message-exposure-py
        raise HTTPException(status_code=500, detail=f"조회 실패: {exc}")  # 예외 내용을 detail 로 노출


@web.errorhandler(Exception)
def handle_error(err):
    # ruleid: mois-4-01-error-message-exposure-py
    return f"오류: {err}", 500  # 예외 내용을 응답 본문에 넣음


@web.route("/orders/<int:order_id>")
def order_page(order_id):
    try:
        return load_order(order_id)
    except KeyError as exc:
        # ruleid: mois-4-01-error-message-exposure-py
        print("order lookup failed", exc)  # 예외를 콘솔에 출력
        return "not found", 404
    finally:
        web.logger.info("order page")


if __name__ == "__main__":
    # ruleid: mois-4-01-error-message-exposure-py
    web.run(debug=True)  # 디버그 모드로 실행
