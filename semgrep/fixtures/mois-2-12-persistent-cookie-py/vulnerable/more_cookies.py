import datetime
from datetime import timedelta

from fastapi import APIRouter, Response
from flask import Flask

app = Flask(__name__)
router = APIRouter()

ONE_YEAR = 60 * 60 * 24 * 365

# Flask 설정: 초로 준 세션 수명
# ruleid: mois-2-12-persistent-cookie-py
app.config["PERMANENT_SESSION_LIFETIME"] = 60 * 60 * 24 * 14
# ruleid: mois-2-12-persistent-cookie-py
app.permanent_session_lifetime = 2592000
# ruleid: mois-2-12-persistent-cookie-py
app.permanent_session_lifetime = timedelta(days=90)


class Config:
    # ruleid: mois-2-12-persistent-cookie-py
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24 * 7
    # Flask-Login "로그인 유지" 쿠키
    # ruleid: mois-2-12-persistent-cookie-py
    REMEMBER_COOKIE_DURATION = timedelta(days=365)


class LegacyConfig:
    # ruleid: mois-2-12-persistent-cookie-py
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=30)


def signed(response, member_id):
    # ruleid: mois-2-12-persistent-cookie-py
    response.set_signed_cookie("member", member_id, salt="member", max_age=ONE_YEAR)
    # ruleid: mois-2-12-persistent-cookie-py
    response.set_signed_cookie("recent", member_id, max_age=timedelta(days=30))
    return response


def by_timedelta(response, request, value):
    # 위치 인자로 준 일수
    # ruleid: mois-2-12-persistent-cookie-py
    response.set_cookie("recent", value, max_age=timedelta(30))
    # 주 단위
    # ruleid: mois-2-12-persistent-cookie-py
    response.set_cookie("auto_login", value, expires=datetime.datetime.now() + timedelta(weeks=4))
    # ruleid: mois-2-12-persistent-cookie-py
    request.session.set_expiry(timedelta(days=14))
    return response


@router.post("/login")
def login(response: Response):
    # Starlette 는 expires 에 초 단위 정수를 받는다
    # ruleid: mois-2-12-persistent-cookie-py
    response.set_cookie(key="sid", value="...", expires=31536000, httponly=True, secure=True)
    return {"result": "ok"}
