from Crypto import Random
from Crypto.Cipher import AES, ARC2, ARC4, CAST, DES3, XOR, Blowfish


def encrypt_3des(key, data):
    # ruleid: mois-2-04-weak-cipher-py
    cipher = DES3.new(key, DES3.MODE_CBC, Random.new().read(8))
    return cipher.encrypt(data)


def encrypt_rc2(key, data):
    # ruleid: mois-2-04-weak-cipher-py
    return ARC2.new(key, ARC2.MODE_CFB, Random.new().read(8)).encrypt(data)


def encrypt_rc4(key, data):
    # ruleid: mois-2-04-weak-cipher-py
    return ARC4.new(key).encrypt(data)


def encrypt_blowfish(key, iv, data):
    # ruleid: mois-2-04-weak-cipher-py
    return Blowfish.new(key, Blowfish.MODE_CBC, iv).encrypt(data)


def encrypt_cast(key, iv, data):
    # ruleid: mois-2-04-weak-cipher-py
    return CAST.new(key, CAST.MODE_OPENPGP, iv).encrypt(data)


def obfuscate(key, data):
    # ruleid: mois-2-04-weak-cipher-py
    return XOR.new(key).encrypt(data)


def encrypt_ecb_keyword(key, data):
    # 운영 모드를 키워드 인자로 준 ECB
    # ruleid: mois-2-04-weak-cipher-py
    return AES.new(key, mode=AES.MODE_ECB).encrypt(data)
