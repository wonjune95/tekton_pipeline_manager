from Crypto.Cipher import AES, ChaCha20_Poly1305
from Cryptodome.Cipher import AES as AES2
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def encrypt_gcm(key, data):
    # ok: mois-2-04-weak-cipher-py AES-GCM
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return cipher.nonce + tag + ciphertext


def encrypt_cbc(key, iv, padded):
    # ok: mois-2-04-weak-cipher-py AES-CBC (운영 모드를 키워드로)
    return AES2.new(key, mode=AES2.MODE_CBC, iv=iv).encrypt(padded)


def encrypt_chacha(key, data):
    # ok: mois-2-04-weak-cipher-py
    cipher = ChaCha20_Poly1305.new(key=key)
    return cipher.nonce + b"".join(cipher.encrypt_and_digest(data))


def encrypt_ctr(key, nonce, data):
    # ok: mois-2-04-weak-cipher-py AES-CTR
    encryptor = Cipher(algorithms.AES(key), modes.CTR(nonce)).encryptor()
    return encryptor.update(data) + encryptor.finalize()
