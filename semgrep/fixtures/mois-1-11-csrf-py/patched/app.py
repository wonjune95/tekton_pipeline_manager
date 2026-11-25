from flask import Flask, request
from flask_login import current_user, login_required
from flask_wtf.csrf import CSRFProtect

from .services import transfer_points

app = Flask(__name__)
# ok: mois-1-11-csrf-py 모든 POST 요청에 CSRF 토큰 검사 적용
csrf = CSRFProtect(app)


@app.route("/points/transfer", methods=["POST"])
@login_required
def transfer():
    transfer_points(current_user.id, request.form["to"], int(request.form["points"]))
    return {"ok": True}
