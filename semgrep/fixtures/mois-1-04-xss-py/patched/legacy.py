"""예전 버전의 flask.escape (Flask 2.2 까지)."""
import flask
from flask import request

app = flask.Flask(__name__)


@app.route("/legacy/escape")
def legacy_escape():
    # ok: mois-1-04-xss-py
    return "<h1>" + flask.escape(request.args.get("name", "")) + "</h1>"
