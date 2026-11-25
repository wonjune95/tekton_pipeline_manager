import os

import jwt
import pymysql
from django.contrib.auth.hashers import check_password


def get_connection():
    # 비밀번호는 환경변수에서 읽는다
    return pymysql.connect(
        host="db.example.org",
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database="portal",
    )


def smtp_password():
    return os.environ.get("SMTP_PASSWORD", "")


def is_admin(password, admin_hash):
    return check_password(password, admin_hash)


def issue_token(payload):
    return jwt.encode(payload, os.environ["JWT_SIGNING_KEY"], algorithm="HS256")


def login_payload(form):
    return {"username": form.get("username", ""), "password": form.get("password", "")}


# 안내 문구·화면 표시 이름은 비밀 값이 아니다
LABELS = {"password": "비밀번호", "new_password": "New password"}
MSG_WRONG_PASSWORD = "Invalid password."
