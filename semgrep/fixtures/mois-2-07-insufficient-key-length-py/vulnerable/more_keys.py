import hashlib
import os
import secrets

import paramiko
from Crypto.PublicKey import DSA, RSA
from Crypto.Random import get_random_bytes
from cryptography.hazmat.primitives.asymmetric import dh, dsa, ec, rsa
from OpenSSL import crypto

KEY_BITS = 1024


def rsa_positional():
    # 위치 인자로 준 키 길이
    # ruleid: mois-2-07-insufficient-key-length-py
    return rsa.generate_private_key(65537, 1024)


def rsa_constant():
    # 모듈 상수로 준 키 길이
    # ruleid: mois-2-07-insufficient-key-length-py
    return RSA.generate(KEY_BITS)


def rsa_bits_keyword():
    # ruleid: mois-2-07-insufficient-key-length-py
    return RSA.generate(bits=1024)


def dsa_keys():
    # ruleid: mois-2-07-insufficient-key-length-py
    a = dsa.generate_private_key(1024)
    # ruleid: mois-2-07-insufficient-key-length-py
    b = dsa.generate_parameters(key_size=1024)
    # ruleid: mois-2-07-insufficient-key-length-py
    c = dsa.generate_parameters(1024)
    # ruleid: mois-2-07-insufficient-key-length-py
    d = DSA.generate(1024)
    # ruleid: mois-2-07-insufficient-key-length-py
    e = DSA.generate(bits=1024)
    return a, b, c, d, e


def dh_parameters():
    # ruleid: mois-2-07-insufficient-key-length-py
    return dh.generate_parameters(generator=2, key_size=1024)


def self_signed_key():
    key = crypto.PKey()
    # pyOpenSSL
    # ruleid: mois-2-07-insufficient-key-length-py
    key.generate_key(crypto.TYPE_RSA, 1024)
    return key


def legacy_dsa_key():
    key = crypto.PKey()
    # ruleid: mois-2-07-insufficient-key-length-py
    key.generate_key(crypto.TYPE_DSA, 1024)
    return key


def ssh_host_key(path):
    # ruleid: mois-2-07-insufficient-key-length-py
    key = paramiko.RSAKey.generate(1024)
    key.write_private_key_file(path)
    # ruleid: mois-2-07-insufficient-key-length-py
    return paramiko.RSAKey.generate(bits=1024)


def weak_curves():
    return [
        # ruleid: mois-2-07-insufficient-key-length-py
        ec.generate_private_key(ec.SECP224R1()),
        # ruleid: mois-2-07-insufficient-key-length-py
        ec.generate_private_key(ec.SECT163K1()),
        # ruleid: mois-2-07-insufficient-key-length-py
        ec.generate_private_key(ec.SECT163R2()),
        # ruleid: mois-2-07-insufficient-key-length-py
        ec.generate_private_key(ec.SECT233K1()),
        # ruleid: mois-2-07-insufficient-key-length-py
        ec.generate_private_key(ec.SECT233R1()),
    ]


class TokenCipher:
    def __init__(self):
        # 속성에 넣는 64비트 키
        # ruleid: mois-2-07-insufficient-key-length-py
        self.key = secrets.token_bytes(8)


def des_style_key():
    # ruleid: mois-2-07-insufficient-key-length-py
    session_key = get_random_bytes(8)
    return session_key


def derive(password, salt):
    # 유도한 키가 64비트
    # ruleid: mois-2-07-insufficient-key-length-py
    a = hashlib.pbkdf2_hmac("sha256", password, salt, 600_000, dklen=8)
    # ruleid: mois-2-07-insufficient-key-length-py
    b = hashlib.pbkdf2_hmac("sha256", password, salt, 600_000, 8)
    # ruleid: mois-2-07-insufficient-key-length-py
    c = hashlib.scrypt(password, salt=salt, n=2**14, r=8, p=1, dklen=12)
    return a, b, c
