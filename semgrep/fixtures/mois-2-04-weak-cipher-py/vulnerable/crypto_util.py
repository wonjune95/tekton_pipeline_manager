from Crypto.Cipher import AES, DES
from Crypto.Util.Padding import pad
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def encrypt_resident_no(key, value):
    # DES 는 취약한 알고리즘
    # ruleid: mois-2-04-weak-cipher-py
    cipher = DES.new(key, DES.MODE_CBC)
    return cipher.iv + cipher.encrypt(pad(value.encode(), DES.block_size))


def encrypt_card_no(key, value):
    # ECB 모드는 같은 평문이 같은 암호문이 된다
    # ruleid: mois-2-04-weak-cipher-py
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pad(value.encode(), AES.block_size))


def encrypt_legacy(key, iv, padded):
    # ruleid: mois-2-04-weak-cipher-py
    encryptor = Cipher(algorithms.TripleDES(key), modes.CBC(iv)).encryptor()
    return encryptor.update(padded) + encryptor.finalize()


def encrypt_block(key, padded):
    # ruleid: mois-2-04-weak-cipher-py
    encryptor = Cipher(algorithms.AES(key), modes.ECB()).encryptor()
    return encryptor.update(padded) + encryptor.finalize()
