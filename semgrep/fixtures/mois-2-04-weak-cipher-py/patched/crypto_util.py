import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def encrypt_resident_no(key, value):
    # AES-GCM (256비트 키), 매번 새 nonce
    nonce = os.urandom(12)
    return nonce + AESGCM(key).encrypt(nonce, value.encode(), None)


def decrypt_resident_no(key, blob):
    return AESGCM(key).decrypt(blob[:12], blob[12:], None).decode()
