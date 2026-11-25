import os

import cx_Oracle

# ruleid: mois-2-13-sensitive-comment-py
# pwd: q1w2e3r4!
# ruleid: mois-2-13-sensitive-comment-py
# 운영 DB 비밀번호는 Portal!2021 (2021-03 변경)
# ruleid: mois-2-13-sensitive-comment-py
# 패스워드 = oper#0412
# 주석 처리한 예전 설정에 값이 남아 있다
# ruleid: mois-2-13-sensitive-comment-py
# DB_PASSWORD = "Portal!2021"
# ruleid: mois-2-13-sensitive-comment-py
# admin passwd is 'tiger'


def connect():
    # ruleid: mois-2-13-sensitive-comment-py
    dsn = os.environ["ORA_DSN"]  # 개발 DB 는 scott / tiger01
    # ruleid: mois-2-13-sensitive-comment-py
    # sqlplus sa/P@ssw0rd 로 접속해서 확인
    return cx_Oracle.connect(os.environ["ORA_USER"], os.environ["ORA_PASSWORD"], dsn)
