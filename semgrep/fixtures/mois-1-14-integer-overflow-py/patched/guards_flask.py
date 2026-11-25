"""guard 형태별 안전한 예제 (Flask)."""
from flask import Flask, abort, request

app = Flask(__name__)
MAX_SIZE = 1024 * 1024


@app.route("/guard/abort")
def guard_abort():
    size = int(request.args.get("size", "0"))
    if size >= MAX_SIZE:
        abort(400)
    # ok: mois-1-14-integer-overflow-py 실패하면 abort
    buf = bytearray(size)
    return bytes(buf)


@app.route("/guard/abort_empty")
def guard_abort_empty():
    size = int(request.args.get("size", "0"))
    if size is None or not 0 <= size <= MAX_SIZE:
        abort(400)
    # ok: mois-1-14-integer-overflow-py 값이 없거나 실패하면 abort
    buf = bytearray(size)
    return bytes(buf)
