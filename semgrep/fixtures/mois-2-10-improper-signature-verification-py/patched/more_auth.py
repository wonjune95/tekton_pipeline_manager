import hmac

import jwt
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from jose import JWTError
from jose import jwt as jose_jwt


def decode(token, key):
    # ok: mois-2-10-improper-signature-verification-py 알고리즘을 정해 두고 서명을 검증
    return jwt.decode(token, key, algorithms=("RS256", "ES256"))


def pyjwt2_options(token, key):
    # ok: mois-2-10-improper-signature-verification-py 서명은 검증하고 aud 만 건너뛴다
    return jwt.decode(token, key, algorithms=["HS256"], options={"verify_aud": False})


def current_user(token, key):
    try:
        claims = jose_jwt.decode(token, key, algorithms=["HS256"])
    # ok: mois-2-10-improper-signature-verification-py 검증 실패는 거부
    except JWTError:
        return None
    return claims.get("sub")


def check_license(pem, document, signature):
    key = RSA.import_key(pem)
    # ok: mois-2-10-improper-signature-verification-py 결과를 조건으로 쓴다
    if not PKCS1_v1_5.new(key).verify(SHA256.new(document), signature):
        raise ValueError("invalid signature")
    return document


def check_callback(secret, body, received):
    expected = hmac.new(secret, body, "sha256").hexdigest()
    # ok: mois-2-10-improper-signature-verification-py 결과를 돌려준다
    return hmac.compare_digest(expected, received)


def kid_of(token):
    # ok: mois-2-10-improper-signature-verification-py 키를 고르려고 헤더만 읽는 것은 검증 생략이 아니다
    return jwt.get_unverified_header(token)["kid"]
