import os

from Crypto.PublicKey import ECC, RSA
from cryptography.hazmat.primitives.asymmetric import dsa, ec, rsa


def new_signing_key():
    # RSA 1024비트는 짧다
    # ruleid: mois-2-07-insufficient-key-length-py
    return rsa.generate_private_key(public_exponent=65537, key_size=1024)


def new_legacy_key():
    # ruleid: mois-2-07-insufficient-key-length-py
    return RSA.generate(1024)


def new_dsa_key():
    # ruleid: mois-2-07-insufficient-key-length-py
    return dsa.generate_private_key(key_size=1024)


def new_ec_key():
    # 192비트 곡선
    # ruleid: mois-2-07-insufficient-key-length-py
    return ec.generate_private_key(ec.SECP192R1())


def new_ecc_key():
    # ruleid: mois-2-07-insufficient-key-length-py
    return ECC.generate(curve="P-192")


def new_data_key():
    # 64비트 대칭키
    # ruleid: mois-2-07-insufficient-key-length-py
    data_key = os.urandom(8)
    return data_key
