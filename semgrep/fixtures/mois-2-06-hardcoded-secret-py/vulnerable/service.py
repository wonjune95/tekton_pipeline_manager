import os

import jwt
import pymysql

# ruleid: mois-2-06-hardcoded-secret-py
API_TOKEN = "9f8a7c6b5d4e3f2a1b0c"


def get_connection():
    # DB 비밀번호가 코드에 있다
    # ruleid: mois-2-06-hardcoded-secret-py
    return pymysql.connect(host="db.example.org", user="portal", password="Portal!2021", database="portal")


def smtp_password():
    # ruleid: mois-2-06-hardcoded-secret-py
    return os.environ.get("SMTP_PASSWORD", "mail1234")


def is_admin(password):
    # ruleid: mois-2-06-hardcoded-secret-py
    return password == "admin!@#$"


def issue_token(payload):
    # ruleid: mois-2-06-hardcoded-secret-py
    return jwt.encode(payload, "my-signing-key", algorithm="HS256")


# 이름이 secret · api_key 로 끝나는 상수
# ruleid: mois-2-06-hardcoded-secret-py
OAUTH_CLIENT_SECRET = "kq3Zx9-portal-oauth"
# ruleid: mois-2-06-hardcoded-secret-py
MAP_API_KEY = "a1b2c3d4e5f60718"


def is_legacy_admin(form):
    # 키 이름이 pwd 인 값을 상수와 비교
    # ruleid: mois-2-06-hardcoded-secret-py
    return form.get("pwd") == "master1234"
