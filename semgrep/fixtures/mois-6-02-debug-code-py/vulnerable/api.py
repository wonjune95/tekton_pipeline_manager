# ruleid: mois-6-02-debug-code-py
import ipdb
# ruleid: mois-6-02-debug-code-py
import pudb
# ruleid: mois-6-02-debug-code-py
from pdb import set_trace
from fastapi import FastAPI

from .services import cancel_order, load_order, mark_notified, notify_buyer, refund_order, release_lock

app = FastAPI()


@app.get("/orders/{order_id}")
def order(order_id: int):
    # ruleid: mois-6-02-debug-code-py
    ipdb.set_trace()
    try:
        found = load_order(order_id)
    except KeyError as exc:
        # ok: mois-6-02-debug-code-py 잡은 예외 출력은 4-1(오류 메시지 정보노출) 규칙이 맡는다
        print("lookup failed", exc)
        return {"error": "E404"}
    else:
        # ruleid: mois-6-02-debug-code-py
        print("found", found)
    return found


@app.get("/orders")
def orders(limit: int = 10):
    # ruleid: mois-6-02-debug-code-py
    pudb.set_trace()
    # ruleid: mois-6-02-debug-code-py
    print("limit", limit, flush=True)
    return []


@app.delete("/orders/{order_id}")
def cancel(order_id: int):
    try:
        cancel_order(order_id)
    except KeyError as exc:
        # ok: mois-6-02-debug-code-py 잡은 예외 출력은 4-1 규칙이 맡는다 (else·finally 없는 try)
        print("cancel failed", exc)
    try:
        refund_order(order_id)
    except ValueError as exc:
        # ok: mois-6-02-debug-code-py (finally 가 붙은 try)
        print("refund failed", exc)
    finally:
        release_lock(order_id)
    try:
        notify_buyer(order_id)
    except OSError as exc:
        # ok: mois-6-02-debug-code-py (else·finally 가 모두 붙은 try)
        print("notify failed", exc)
    else:
        mark_notified(order_id)
    finally:
        release_lock(order_id)
    return {"cancelled": order_id}


# 서버를 띄우지 않고 값만 찍어 보는 블록
# ruleid: mois-6-02-debug-code-py
if __name__ == "__main__":
    result = orders(3)
    assert result == []
