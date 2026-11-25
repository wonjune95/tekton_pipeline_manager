from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Response
from flask import Flask

app = Flask(__name__)
router = APIRouter()

# ok: mois-2-12-persistent-cookie-py 30분
app.permanent_session_lifetime = timedelta(minutes=30)


class Config:
    # ok: mois-2-12-persistent-cookie-py 하루
    PERMANENT_SESSION_LIFETIME = 86400
    # ok: mois-2-12-persistent-cookie-py 하루
    REMEMBER_COOKIE_DURATION = timedelta(days=1)


def signed(response, member_id):
    # ok: mois-2-12-persistent-cookie-py 한 시간
    response.set_signed_cookie("member", member_id, salt="member", max_age=3600)
    # ok: mois-2-12-persistent-cookie-py 12시간 뒤 만료
    response.set_cookie("recent", member_id, expires=datetime.now(timezone.utc) + timedelta(hours=12))
    return response


@router.post("/layout")
def choose_layout(response: Response):
    # ok: mois-2-12-persistent-cookie-py 만료를 주지 않은 세션 쿠키
    response.set_cookie(key="layout", value="wide", httponly=True, secure=True)
    return {"result": "ok"}
