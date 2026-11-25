"""예전 버전에 있던 Markup 재수출 (flask.Markup: Flask 2.2 까지, jinja2.Markup: Jinja2 3.0 까지)."""
import flask
import jinja2
from flask import request

app = flask.Flask(__name__)


@app.route("/legacy/markup")
def legacy_markup():
    name = request.args.get("name", "")
    # ruleid: mois-1-04-xss-py
    first = flask.Markup("<b>" + name + "</b>")
    # ruleid: mois-1-04-xss-py
    second = jinja2.Markup("<i>%s</i>" % name)
    return flask.render_template("badge.html", first=first, second=second)
