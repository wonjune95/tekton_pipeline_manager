# 공통 source 블록 시험 (감사 사례). `# CASE` 표시만 있고 ruleid 가 없는 줄은 알려진 미탐 — 공통 source 가 보지 않는 형태다.
import os
from datetime import datetime

import flask
from flask import Blueprint, Flask, request
from flask import request as flask_request
from flask.views import MethodView
from flask_login import login_required

app = Flask(__name__)
bp = Blueprint("bp", __name__)


@app.route("/c1")
def ctl_args():
    x = request.args.get("x")
    # ruleid: mois-1-05-os-command-injection-py — ctl-flask-args
    os.system(x)


@app.route("/c2")
def ctl_headers():
    x = request.headers["X-Cmd"]
    # ruleid: mois-1-05-os-command-injection-py — ctl-flask-headers-subscript
    os.system(x)


@app.route("/c3")
def ctl_cookies():
    x = request.cookies.get("c")
    # ruleid: mois-1-05-os-command-injection-py — ctl-flask-cookies
    os.system(x)


@app.route("/c4")
def ctl_get_json():
    x = request.get_json()["x"]
    # ruleid: mois-1-05-os-command-injection-py — ctl-flask-get_json
    os.system(x)


@app.route("/c5")
def ctl_values():
    x = request.values["x"]
    # ruleid: mois-1-05-os-command-injection-py — ctl-flask-values
    os.system(x)


@app.route("/c6")
def ctl_flask_dot_request():
    x = flask.request.form["x"]
    # ruleid: mois-1-05-os-command-injection-py — ctl-flask.request-form
    os.system(x)


@app.route("/c7")
def ctl_files():
    x = request.files["f"].filename
    # ruleid: mois-1-05-os-command-injection-py — ctl-flask-files-filename
    os.system(x)


@app.route("/m1")
def miss_referrer():
    x = request.referrer
    # ruleid: mois-1-05-os-command-injection-py — flask-referrer
    os.system(x)


@app.route("/m2")
def miss_host():
    x = request.host
    os.system(x)  # CASE flask-host


@app.route("/m3")
def miss_environ():
    x = request.environ["HTTP_X_CMD"]
    # ruleid: mois-1-05-os-command-injection-py — flask-environ
    os.system(x)


@app.route("/m4")
def miss_user_agent():
    x = request.user_agent.string
    # ruleid: mois-1-05-os-command-injection-py — flask-user_agent
    os.system(x)


@app.route("/m5")
def miss_authorization():
    x = request.authorization.username
    # ruleid: mois-1-05-os-command-injection-py — flask-authorization-username
    os.system(x)


@app.route("/m6")
def miss_base_url():
    x = request.base_url
    os.system(x)  # CASE flask-base_url


@app.route("/m7")
def miss_alias():
    x = flask_request.args["x"]
    # ruleid: mois-1-05-os-command-injection-py — flask-request-import-alias
    os.system(x)


@app.route("/m8")
def miss_content_type():
    x = request.content_type
    # ruleid: mois-1-05-os-command-injection-py — flask-content_type
    os.system(x)


@app.route("/m9")
def miss_access_route():
    x = request.access_route[0]
    os.system(x)  # CASE flask-access_route


@bp.route("/r1/<name>")
def ctl_bp_route(name):
    # ruleid: mois-1-05-os-command-injection-py — ctl-bp.route-param
    os.system(name)


@app.get("/r2/<name>")
def ctl_app_get(name):
    # ruleid: mois-1-05-os-command-injection-py — ctl-flask-app.get-param
    os.system(name)


@app.route("/r3/<name>")
@login_required
def ctl_stacked(name):
    # ruleid: mois-1-05-os-command-injection-py — ctl-flask-route-stacked-decorator
    os.system(name)


@app.route("/r4/<name>")
def ctl_typed_str(name: str):
    # ruleid: mois-1-05-os-command-injection-py — ctl-flask-route-param-str
    os.system(name)


@app.route("/kill/<pid>")
def miss_flask_int(pid: int):
    # ruleid: mois-1-05-os-command-injection-py — flask-route-param-annotated-int-not-enforced
    os.system(f"kill {pid}")


@app.route("/logs/<day>")
def miss_flask_date(day: datetime):
    # ruleid: mois-1-05-os-command-injection-py — flask-route-param-annotated-datetime-not-enforced
    os.system(f"zcat /var/log/app/{day}.gz")


@app.route("/r5/<name>")
def miss_kwargs(**kwargs):
    os.system(kwargs["name"])  # CASE flask-route-kwargs


class ToolView(MethodView):
    def get(self, name):
        os.system(name)  # CASE flask-MethodView-param


app.add_url_rule("/tool/<name>", view_func=ToolView.as_view("tool"))


def plain_view(name):
    os.system(name)  # CASE flask-add_url_rule-param


app.add_url_rule("/plain/<name>", view_func=plain_view)
