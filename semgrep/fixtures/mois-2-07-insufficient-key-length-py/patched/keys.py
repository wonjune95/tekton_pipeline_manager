import os

from Crypto.PublicKey import ECC, RSA
from cryptography.hazmat.primitives.asymmetric import ec, rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def new_signing_key():
    return rsa.generate_private_key(public_exponent=65537, key_size=3072)


def new_legacy_key():
    return RSA.generate(2048)


def new_ec_key():
    return ec.generate_private_key(ec.SECP256R1())


def new_ecc_key():
    return ECC.generate(curve="P-256")


def new_data_key():
    data_key = AESGCM.generate_key(bit_length=256)
    nonce = os.urandom(12)
    return data_key, nonce
