import pyDes
from pyDes import triple_des


def encrypt_phone(key, phone):
    # ruleid: mois-2-04-weak-cipher-py
    k = pyDes.des(key, pyDes.CBC, b"\0" * 8, padmode=pyDes.PAD_PKCS5)
    return k.encrypt(phone)


def encrypt_account(key, account):
    # ruleid: mois-2-04-weak-cipher-py
    return triple_des(key, padmode=pyDes.PAD_PKCS5).encrypt(account)
