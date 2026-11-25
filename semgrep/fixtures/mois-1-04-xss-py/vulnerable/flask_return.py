"""Flask 뷰가 입력이 든 값을 그대로 반환 — 문자열은 text/html 로 응답된다."""
import flask
from flask import Blueprint, Flask, jsonify, make_response, request

app = Flask(__name__)
bp = Blueprint("pages", __name__)


@app.route("/var")
def return_variable():
    name = request.args["name"]
    body = "<h1>Hello " + name + "</h1>"
    # 변수에 담아 반환해도 같다
    # ruleid: mois-1-04-xss-py
    return body


@app.route("/bare")
def return_bare_value():
    # ruleid: mois-1-04-xss-py
    return request.args["name"]


@app.route("/bare-call")
def return_request_call():
    # request 로 시작하는 호출은 문자열이다
    # ruleid: mois-1-04-xss-py
    return request.args.get("name", "")


@app.route("/bare-call-module")
def return_module_request_call():
    # ruleid: mois-1-04-xss-py
    return flask.request.args.get("name", "")


@app.route("/format")
def return_format_call():
    name = request.args["name"]
    # 문자열 리터럴의 메서드 호출
    # ruleid: mois-1-04-xss-py
    return "<h1>Hello {}</h1>".format(name)


@app.route("/tuple")
def return_variable_tuple():
    msg = "<h1>Hello {}</h1>".format(request.args["name"])
    # ruleid: mois-1-04-xss-py
    return msg, 200


@app.route("/json-in-script")
def json_body_in_script():
    name = request.args["name"]
    # jsonify 의 본문을 꺼내 HTML 에 넣으면 JSON 응답이 아니다 (</script> 로 빠져나온다)
    # ruleid: mois-1-04-xss-py
    return make_response("<script>var d = " + jsonify(name=name).get_data(as_text=True) + "</script>")


# 같은 파일에서 Flask(...)·Blueprint(...) 로 만든 객체의 메서드별 라우트 — 태그가 없는 문자열도 text/html 이다
@app.get("/hello")
def flask_get():
    name = request.args["name"]
    # ruleid: mois-1-04-xss-py
    return "Hello " + name


@app.post("/hello")
def flask_post():
    # ruleid: mois-1-04-xss-py
    return "Hello " + request.form["name"]


@bp.put("/hello")
def blueprint_put():
    name = request.form["name"]
    # ruleid: mois-1-04-xss-py
    return name


@bp.patch("/hello")
def blueprint_patch():
    # ruleid: mois-1-04-xss-py
    return "수정됨: %s" % request.form["name"]


@bp.delete("/hello")
def blueprint_delete():
    # ruleid: mois-1-04-xss-py
    return request.args["name"] + " 삭제됨"
