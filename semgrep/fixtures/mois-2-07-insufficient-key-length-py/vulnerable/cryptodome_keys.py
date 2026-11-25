from Cryptodome.PublicKey import DSA, ECC, RSA
from Cryptodome.Random import get_random_bytes


def keys():
    # ruleid: mois-2-07-insufficient-key-length-py
    a = RSA.generate(1024)
    # ruleid: mois-2-07-insufficient-key-length-py
    b = RSA.generate(bits=512)
    # ruleid: mois-2-07-insufficient-key-length-py
    c = DSA.generate(1024)
    # ruleid: mois-2-07-insufficient-key-length-py
    d = DSA.generate(bits=1024)
    # ruleid: mois-2-07-insufficient-key-length-py
    e = ECC.generate(curve="secp224r1")
    return a, b, c, d, e


def data_key():
    # ruleid: mois-2-07-insufficient-key-length-py
    aes_key = get_random_bytes(8)
    return aes_key
