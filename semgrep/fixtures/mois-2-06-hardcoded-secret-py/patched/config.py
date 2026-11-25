import os

import jwt
import redis
from pydantic_settings import BaseSettings

# ok: mois-2-06-hardcoded-secret-py 기본값 없이 환경변수에서만 읽는다
ADMIN_PWD = os.getenv("ADMIN_PWD")


class Settings(BaseSettings):
    db_host: str = "db.example.org"
    # ok: mois-2-06-hardcoded-secret-py 값은 환경변수·비밀 저장소가 채운다
    db_password: str


class MailClient:
    def __init__(self, host, password):
        self.host = host
        # ok: mois-2-06-hardcoded-secret-py 밖에서 받은 값
        self.smtp_password = password


def cache():
    # ok: mois-2-06-hardcoded-secret-py
    return redis.Redis(host="cache.example.org", password=os.environ["REDIS_PASSWORD"])


def engine_url():
    # ok: mois-2-06-hardcoded-secret-py 자리표시자가 들어간 접속 문자열
    return "postgresql://{user}:{password}@db.example.org/portal".format(
        user=os.environ["DB_USER"], password=os.environ["DB_PASSWORD"]
    )


def public_url():
    # ok: mois-2-06-hardcoded-secret-py 계정이 없는 주소
    return "https://api.example.org:8443/v1/members"


def password_field_type(show_password):
    # ok: mois-2-06-hardcoded-secret-py 비밀번호 값이 아니라 화면 표시 여부
    return "text" if show_password == "true" else "password"


def read_token(token, key):
    # ok: mois-2-06-hardcoded-secret-py 키를 밖에서 받는다
    return jwt.decode(token, key, algorithms=["HS256"])
