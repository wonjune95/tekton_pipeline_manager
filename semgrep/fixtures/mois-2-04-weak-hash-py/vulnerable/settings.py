PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    # 솔트 없는 MD5 해셔 허용
    # ruleid: mois-2-04-weak-hash-py
    "django.contrib.auth.hashers.UnsaltedMD5PasswordHasher",
    # 옛 DB 를 옮기며 남겨 둔 해셔들
    # ruleid: mois-2-04-weak-hash-py
    "django.contrib.auth.hashers.MD5PasswordHasher",
    # ruleid: mois-2-04-weak-hash-py
    "django.contrib.auth.hashers.SHA1PasswordHasher",
    # ruleid: mois-2-04-weak-hash-py
    "django.contrib.auth.hashers.UnsaltedSHA1PasswordHasher",
    # ruleid: mois-2-04-weak-hash-py
    "django.contrib.auth.hashers.CryptPasswordHasher",
]
