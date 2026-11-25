import os

import pymysql


# ruleid: mois-2-13-sensitive-comment-py
# DB연결 root / a1q2w3r3f2!@
def connect():
    return pymysql.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )


def admin_connect():
    # ruleid: mois-2-13-sensitive-comment-py
    # Password for administrator is "tiger."
    return pymysql.connect(host=os.environ["DB_HOST"], user="admin", password=os.environ["DB_ADMIN_PASSWORD"])


def sample():
    # ruleid: mois-2-13-sensitive-comment-py
    return "sample"  # 암호화 전, 후 : 1365ADMIN_01, aa84c40031d808196537ad3dcf81f9af


# ruleid: mois-2-13-sensitive-comment-py
# 운영 콘솔 계정 admin/Portal2021!
def console_url():
    return os.environ["CONSOLE_URL"]
