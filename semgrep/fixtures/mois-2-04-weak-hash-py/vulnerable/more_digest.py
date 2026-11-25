import hashlib
import hmac

from Crypto.Hash import MD2, MD4, SHA, SHA1
from Cryptodome.Hash import MD5 as CMD5
from Cryptodome.Hash import SHA1 as CSHA1
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


def named_sha1(data):
    # ruleid: mois-2-04-weak-hash-py
    h = hashlib.new("sha1")
    h.update(data)
    return h.hexdigest()


def sign_md5(key, message):
    # ruleid: mois-2-04-weak-hash-py
    return hmac.new(key, message, hashlib.md5).hexdigest()


def sign_md5_keyword(key, message):
    # ruleid: mois-2-04-weak-hash-py
    return hmac.new(key, msg=message, digestmod=hashlib.md5).digest()


def sign_sha1_keyword(key, message):
    # ruleid: mois-2-04-weak-hash-py
    return hmac.new(key, message, digestmod=hashlib.sha1).digest()


def sign_by_name(key, message):
    # 해시 이름을 문자열로 준 경우
    # ruleid: mois-2-04-weak-hash-py
    a = hmac.new(key, message, "md5").digest()
    # ruleid: mois-2-04-weak-hash-py
    b = hmac.new(key, message, digestmod="sha1").digest()
    # ruleid: mois-2-04-weak-hash-py
    c = hmac.digest(key, message, "md5")
    return a, b, c


def pycrypto_digests(data):
    # ruleid: mois-2-04-weak-hash-py
    a = MD2.new(data).hexdigest()
    # ruleid: mois-2-04-weak-hash-py
    b = MD4.new(data).hexdigest()
    # ruleid: mois-2-04-weak-hash-py
    c = SHA.new(data).hexdigest()
    # ruleid: mois-2-04-weak-hash-py
    d = SHA1.new(data).hexdigest()
    return a, b, c, d


def cryptodome_digests(data):
    # ruleid: mois-2-04-weak-hash-py
    a = CMD5.new(data).hexdigest()
    # ruleid: mois-2-04-weak-hash-py
    b = CSHA1.new(data).hexdigest()
    return a, b


def sign_document(private_key, document):
    # ruleid: mois-2-04-weak-hash-py
    return private_key.sign(document, padding.PKCS1v15(), hashes.MD5())


def legacy_named_digests(password, cert_der, data):
    # NTLM 해시 (MD4)
    # ruleid: mois-2-04-weak-hash-py
    ntlm = hashlib.new("md4", password.encode("utf-16le")).hexdigest()
    # 옛 인증서 지문 (MD2)
    # ruleid: mois-2-04-weak-hash-py
    fingerprint = hashlib.new("md2", cert_der).hexdigest()
    # OpenSSL 의 옛 이름 "sha" 는 SHA-0
    # ruleid: mois-2-04-weak-hash-py
    legacy = hashlib.new("sha", data).hexdigest()
    return ntlm, fingerprint, legacy
