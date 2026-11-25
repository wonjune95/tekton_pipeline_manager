import hashlib
import hmac

from cryptography.hazmat.primitives import hashes


def token_digest(token):
    return hashlib.sha256(token.encode()).hexdigest()


def cache_key(url):
    # 보안 용도가 아닌 캐시 키
    return hashlib.md5(url.encode(), usedforsecurity=False).hexdigest()


def sign_message(key, message):
    return hmac.new(key, message, hashlib.sha256).hexdigest()


def certificate_hash():
    return hashes.SHA256()
