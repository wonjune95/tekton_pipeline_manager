import os

import joblib
from flask import Flask, abort, request

app = Flask(__name__)
MODEL_DIR = "/var/app/models"
MODELS = {"churn", "fraud"}


@app.get("/v2/or-none")
def guard_joined_with_none_check():
    name = request.args.get("model")
    if name is None or name not in MODELS:
        abort(404)
    # ok: mois-5-05-insecure-deserialization-py None 검사와 or 로 묶은 허용 목록 guard
    return {"model": str(joblib.load(os.path.join(MODEL_DIR, name + ".joblib")))}
