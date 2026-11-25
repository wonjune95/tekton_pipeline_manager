import hmac
import os

import jwt
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

SECRET = os.environ["JWT_SECRET"]


def read_claims(token):
    # 서명을 검증하지 않고 내용을 믿는다
    # ruleid: mois-2-10-improper-signature-verification-py
    return jwt.decode(token, options={"verify_signature": False})


def read_claims_legacy(token):
    # ruleid: mois-2-10-improper-signature-verification-py
    return jwt.decode(token, SECRET, verify=False)


def read_claims_any(token):
    # 서명 없는 토큰(alg=none)도 통과
    # ruleid: mois-2-10-improper-signature-verification-py
    return jwt.decode(token, SECRET, algorithms=["HS256", "none"])


def check_webhook(expected, received, body):
    # 비교 결과를 쓰지 않는다
    # ruleid: mois-2-10-improper-signature-verification-py
    hmac.compare_digest(expected, received)
    return body


def check_update(public_key, signature, data):
    # ruleid: mois-2-10-improper-signature-verification-py
    try:
        public_key.verify(signature, data, padding.PKCS1v15(), hashes.SHA256())
    except InvalidSignature:
        pass
    return data
