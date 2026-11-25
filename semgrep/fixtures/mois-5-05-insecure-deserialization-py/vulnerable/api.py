import base64
import marshal

import jsonpickle
from fastapi import FastAPI
from flask import Flask, request

api = FastAPI()
web = Flask(__name__)


@api.post("/session/restore")
def restore(state: str):
    # 요청 값을 jsonpickle 로 복원
    # ruleid: mois-5-05-insecure-deserialization-py
    return {"user": jsonpickle.decode(state).user}


@web.route("/task", methods=["POST"])
def run_task():
    # ruleid: mois-5-05-insecure-deserialization-py
    code = marshal.loads(base64.b64decode(request.get_data()))  # 요청 본문을 marshal 로 역직렬화
    return {"size": len(code.co_code)}
