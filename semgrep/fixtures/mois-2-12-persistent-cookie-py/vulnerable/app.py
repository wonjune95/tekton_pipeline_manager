from datetime import timedelta

from flask import Flask, make_response

app = Flask(__name__)
# ruleid: mois-2-12-persistent-cookie-py
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=31)


@app.route("/theme/<name>")
def theme(name):
    resp = make_response("ok")
    # ruleid: mois-2-12-persistent-cookie-py
    resp.set_cookie("recent_member", name, 31536000)
    return resp
