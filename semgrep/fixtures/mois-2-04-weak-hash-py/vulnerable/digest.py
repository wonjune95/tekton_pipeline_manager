import hashlib
import hmac

from Crypto.Hash import MD5
from cryptography.hazmat.primitives import hashes


def token_digest(token):
    # MD5 는 충돌에 취약
    # ruleid: mois-2-04-weak-hash-py
    return hashlib.md5(token.encode()).hexdigest()


def file_fingerprint(data):
    # ruleid: mois-2-04-weak-hash-py
    return hashlib.sha1(data).hexdigest()


def named_digest(data):
    # ruleid: mois-2-04-weak-hash-py
    return hashlib.new("md5", data).hexdigest()


def sign_message(key, message):
    # ruleid: mois-2-04-weak-hash-py
    return hmac.new(key, message, hashlib.sha1).hexdigest()


def legacy_digest(data):
    # ruleid: mois-2-04-weak-hash-py
    return MD5.new(data).hexdigest()


def certificate_hash():
    # ruleid: mois-2-04-weak-hash-py
    return hashes.SHA1()
