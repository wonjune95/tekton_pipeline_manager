from Cryptodome.Cipher import ARC2, ARC4, CAST, DES, DES3, Blowfish
from Cryptodome.Random import get_random_bytes


def des_encrypt(key, data):
    # ruleid: mois-2-04-weak-cipher-py
    cipher = DES.new(key, DES.MODE_OFB)
    return cipher.iv + cipher.encrypt(data)


def des3_encrypt(key, data):
    # ruleid: mois-2-04-weak-cipher-py
    cipher = DES3.new(key, DES3.MODE_CFB)
    return cipher.iv + cipher.encrypt(data)


def rc2_encrypt(key, data):
    # ruleid: mois-2-04-weak-cipher-py
    return ARC2.new(key, ARC2.MODE_CBC, get_random_bytes(8)).encrypt(data)


def rc4_encrypt(key, data):
    # ruleid: mois-2-04-weak-cipher-py
    return ARC4.new(key).encrypt(data)


def blowfish_encrypt(key, data):
    # ruleid: mois-2-04-weak-cipher-py
    return Blowfish.new(key, Blowfish.MODE_CBC).encrypt(data)


def cast_encrypt(key, data):
    # ruleid: mois-2-04-weak-cipher-py
    return CAST.new(key, CAST.MODE_OPENPGP).encrypt(data)
