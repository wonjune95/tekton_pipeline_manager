from cryptography.hazmat.decrepit.ciphers import algorithms as old
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def blowfish(key, iv):
    # ruleid: mois-2-04-weak-cipher-py
    return Cipher(algorithms.Blowfish(key), modes.CBC(iv)).encryptor()


def rc4(key):
    # ruleid: mois-2-04-weak-cipher-py
    return Cipher(algorithms.ARC4(key), mode=None).encryptor()


def idea(key, iv):
    # ruleid: mois-2-04-weak-cipher-py
    return Cipher(algorithms.IDEA(key), modes.CBC(iv)).encryptor()


def cast5(key, iv):
    # ruleid: mois-2-04-weak-cipher-py
    return Cipher(algorithms.CAST5(key), modes.CBC(iv)).encryptor()


# cryptography 43 부터 취약 알고리즘은 decrepit 모듈로 옮겨졌다
def decrepit_3des(key, iv):
    # ruleid: mois-2-04-weak-cipher-py
    return Cipher(old.TripleDES(key), modes.CBC(iv)).encryptor()


def decrepit_blowfish(key, iv):
    # ruleid: mois-2-04-weak-cipher-py
    return Cipher(old.Blowfish(key), modes.CBC(iv)).encryptor()


def decrepit_rc4(key):
    # ruleid: mois-2-04-weak-cipher-py
    return Cipher(old.ARC4(key), mode=None).encryptor()


def decrepit_idea(key, iv):
    # ruleid: mois-2-04-weak-cipher-py
    return Cipher(old.IDEA(key), modes.CBC(iv)).encryptor()


def decrepit_cast5(key, iv):
    # ruleid: mois-2-04-weak-cipher-py
    return Cipher(old.CAST5(key), modes.CBC(iv)).encryptor()
