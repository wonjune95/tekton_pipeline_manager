"""Flask 2.0 이하의 flask.safe_join (이후 werkzeug.utils.safe_join 으로 옮겨짐)."""
import flask

app = flask.Flask(__name__)
DOCS_DIR = "/srv/docs"


@app.route("/docs/<path:name>")
def docs(name):
    # ok: mois-1-03-path-traversal-py 기준 디렉터리를 벗어나면 NotFound 를 낸다
    return flask.send_file(flask.safe_join(DOCS_DIR, name))
