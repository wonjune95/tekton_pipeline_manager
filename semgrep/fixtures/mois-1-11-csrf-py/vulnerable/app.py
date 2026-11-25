from flask import Flask, request
from flask_login import current_user, login_required
from flask_wtf.csrf import CSRFProtect

from .services import transfer_points

app = Flask(__name__)
# 폼 CSRF 검사를 전역으로 끔
# ruleid: mois-1-11-csrf-py
app.config["WTF_CSRF_ENABLED"] = False
csrf = CSRFProtect(app)


# ruleid: mois-1-11-csrf-py
@app.route("/points/transfer", methods=["POST"])
@csrf.exempt  # 이 뷰만 CSRF 검사 제외
@login_required
def transfer():
    transfer_points(current_user.id, request.form["to"], int(request.form["points"]))
    return {"ok": True}
