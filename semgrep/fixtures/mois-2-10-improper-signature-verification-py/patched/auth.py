import hmac
import logging
import os

import jwt
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

logger = logging.getLogger(__name__)
SECRET = os.environ["JWT_SECRET"]


def read_claims(token):
    # 서명과 알고리즘을 검증한다 (실패하면 jwt.InvalidTokenError)
    return jwt.decode(token, SECRET, algorithms=["HS256"])


def check_webhook(expected, received, body):
    if not hmac.compare_digest(expected, received):
        raise PermissionError("invalid webhook signature")
    return body


def check_update(public_key, signature, data):
    try:
        public_key.verify(signature, data, padding.PKCS1v15(), hashes.SHA256())
    except InvalidSignature:
        logger.warning("update signature verification failed")
        return None
    return data
