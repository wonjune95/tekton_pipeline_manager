import hashlib
import os
import secrets

import paramiko
from Crypto.PublicKey import DSA
from cryptography.hazmat.primitives.asymmetric import dh, dsa, rsa
from OpenSSL import crypto

KEY_BITS = 3072


def rsa_positional():
    # ok: mois-2-07-insufficient-key-length-py 2048비트
    return rsa.generate_private_key(65537, 2048)


def rsa_constant():
    # ok: mois-2-07-insufficient-key-length-py 모듈 상수 3072
    return rsa.generate_private_key(public_exponent=65537, key_size=KEY_BITS)


def dsa_keys():
    # ok: mois-2-07-insufficient-key-length-py
    return dsa.generate_private_key(2048), DSA.generate(2048)


def dh_parameters():
    # ok: mois-2-07-insufficient-key-length-py
    return dh.generate_parameters(generator=2, key_size=2048)


def self_signed_key():
    key = crypto.PKey()
    # ok: mois-2-07-insufficient-key-length-py
    key.generate_key(crypto.TYPE_RSA, 4096)
    return key


def ssh_host_key():
    # ok: mois-2-07-insufficient-key-length-py
    return paramiko.RSAKey.generate(4096)


def new_data_key():
    # ok: mois-2-07-insufficient-key-length-py 256비트 키
    data_key = secrets.token_bytes(32)
    # ok: mois-2-07-insufficient-key-length-py 키가 아닌 값(IV·솔트)은 길이 기준이 다르다
    iv = os.urandom(12)
    return data_key, iv


def derive(password, salt):
    # ok: mois-2-07-insufficient-key-length-py 256비트 키 유도
    return hashlib.pbkdf2_hmac("sha256", password, salt, 600_000, dklen=32)
