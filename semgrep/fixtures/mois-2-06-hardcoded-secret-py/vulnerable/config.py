import os

import jwt
import redis
from pydantic_settings import BaseSettings

# ruleid: mois-2-06-hardcoded-secret-py
ADMIN_PWD = os.getenv("ADMIN_PWD", "admin1234")

# 소스에 넣어 둔 개인키
# ruleid: mois-2-06-hardcoded-secret-py
SIGNING_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAxQ1examplekeymaterialonlyforfixture
-----END RSA PRIVATE KEY-----"""


class Settings(BaseSettings):
    db_host: str = "db.example.org"
    # 타입 표기가 있는 기본값
    # ruleid: mois-2-06-hardcoded-secret-py
    db_password: str = "Portal!2021"


class MailClient:
    def __init__(self, host):
        self.host = host
        # 속성에 넣은 상수 비밀번호
        # ruleid: mois-2-06-hardcoded-secret-py
        self.smtp_password = "Mail!2345"


def cache():
    # ruleid: mois-2-06-hardcoded-secret-py
    return redis.Redis(host="cache.example.org", password="r3dis-pass")


def storage_options():
    # ruleid: mois-2-06-hardcoded-secret-py
    return {"aws_access_key_id": "AKIAEXAMPLE", "aws_secret_access_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCY"}


def check_backdoor(request, user):
    # 상수가 왼쪽에 온 비교
    # ruleid: mois-2-06-hardcoded-secret-py
    if "letmein!2021" == request.POST.get("password"):
        return True
    # 속성과 비교, 같지 않음 비교
    # ruleid: mois-2-06-hardcoded-secret-py
    if user.passwd != "master!key":
        return False
    return True


def read_token(token):
    # ruleid: mois-2-06-hardcoded-secret-py
    return jwt.decode(token, "my-signing-key", algorithms=["HS256"])


def engine_url():
    # ruleid: mois-2-06-hardcoded-secret-py
    return "postgresql+psycopg2://portal:Portal!2021@db.example.org:5432/portal"
