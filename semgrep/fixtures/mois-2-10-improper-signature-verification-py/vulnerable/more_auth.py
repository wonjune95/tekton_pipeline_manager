import hmac

import jwt
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_PSS, PKCS1_v1_5
from itsdangerous import BadSignature, SignatureExpired, URLSafeSerializer, URLSafeTimedSerializer
from jose import JWTError, jws
from jose import jwt as jose_jwt


def claims_without_check(token):
    # python-jose: 서명 확인 없이 내용만 꺼낸다
    # ruleid: mois-2-10-improper-signature-verification-py
    return jose_jwt.get_unverified_claims(token)


def jws_claims_without_check(token):
    # ruleid: mois-2-10-improper-signature-verification-py
    return jws.get_unverified_claims(token)


def decode_any(token, key):
    # ruleid: mois-2-10-improper-signature-verification-py
    a = jwt.decode(token, key, algorithms=("none", "HS256"))
    # ruleid: mois-2-10-improper-signature-verification-py
    b = jwt.decode(token, key, algorithms="none")
    return a, b


def issue_unsigned(payload):
    # 서명 없는 토큰을 발급
    # ruleid: mois-2-10-improper-signature-verification-py
    return jwt.encode(payload, None, algorithm="none")


def pyjwt2_options(token, key):
    # 옵션 dict 를 따로 만든 경우 (탐지 위치는 dict 줄)
    # ruleid: mois-2-10-improper-signature-verification-py
    opts = {"verify_signature": False, "verify_exp": True}
    return jwt.decode(token, key, algorithms=["HS256"], options=opts)


def current_user(token, key):
    claims = {}
    # 검증 실패를 무시하고 계속 진행
    # ruleid: mois-2-10-improper-signature-verification-py
    try:
        claims = jose_jwt.decode(token, key, algorithms=["HS256"])
    except JWTError:
        pass
    return claims.get("sub", "guest")


def read_cookie(serializer: URLSafeSerializer, value):
    data = None
    # ruleid: mois-2-10-improper-signature-verification-py
    try:
        data = serializer.loads(value)
    except BadSignature as exc:
        pass
    return data


def pyjwt_errors(token, key):
    # ruleid: mois-2-10-improper-signature-verification-py
    try:
        return jwt.decode(token, key, algorithms=["RS256"])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        pass


def check_license(pem, document, signature):
    key = RSA.import_key(pem)
    digest = SHA256.new(document)
    # verify() 가 돌려준 True/False 를 버린다
    # ruleid: mois-2-10-improper-signature-verification-py
    PKCS1_v1_5.new(key).verify(digest, signature)
    # ruleid: mois-2-10-improper-signature-verification-py
    PKCS1_PSS.new(key).verify(digest, signature)
    return document


def check_callback(secret, body, received):
    expected = hmac.new(secret, body, "sha256").hexdigest()
    # 결과를 쓰지 않는 비교 (들여쓰기 안쪽)
    if received:
        # ruleid: mois-2-10-improper-signature-verification-py
        hmac.compare_digest(expected, received)
    return body


# 라이브러리별 검증 실패 예외를 무시하는 경우 (예외 이름마다 하나씩)
def expired_is_fine(token, key):
    # 만료된 서명을 무시
    # ruleid: mois-2-10-improper-signature-verification-py
    try:
        return jwt.decode(token, key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        pass


def any_token_error(token, key):
    claims = {}
    # PyJWT 의 검증 실패 예외 전체를 무시
    # ruleid: mois-2-10-improper-signature-verification-py
    try:
        claims = jwt.decode(token, key, algorithms=["HS256"])
    except jwt.InvalidTokenError as exc:
        pass
    return claims


def broken_token(token, key):
    # 서명 부분이 깨진 토큰을 무시
    # ruleid: mois-2-10-improper-signature-verification-py
    try:
        return jwt.decode(token, key, algorithms=["HS256"])
    except jwt.DecodeError:
        pass


def read_timed_cookie(serializer: URLSafeTimedSerializer, value):
    data = None
    # itsdangerous: 유효 기간이 지난 서명을 무시
    # ruleid: mois-2-10-improper-signature-verification-py
    try:
        data = serializer.loads(value, max_age=3600)
    except SignatureExpired:
        pass
    return data
