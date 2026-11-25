import hashlib
import hmac

from Crypto.Hash import SHA256
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


def etag(body):
    # ok: mois-2-04-weak-hash-py 보안 용도가 아님을 표시
    return hashlib.new("md5", body, usedforsecurity=False).hexdigest()


def sign_by_name(key, message):
    # ok: mois-2-04-weak-hash-py SHA-256
    a = hmac.new(key, message, "sha256").digest()
    # ok: mois-2-04-weak-hash-py
    b = hmac.new(key, message, digestmod=hashlib.sha512).digest()
    # ok: mois-2-04-weak-hash-py
    c = hmac.digest(key, message, "sha3_256")
    return a, b, c


def pycrypto_digest(data):
    # ok: mois-2-04-weak-hash-py
    return SHA256.new(data).hexdigest()


def named_sha256(data):
    # ok: mois-2-04-weak-hash-py 이름이 sha1 로 시작하지 않는다 (sha256·sha3_256)
    return hashlib.new("sha256", data).hexdigest()


def sign_document(private_key, document):
    # ok: mois-2-04-weak-hash-py
    return private_key.sign(document, padding.PKCS1v15(), hashes.SHA256())
