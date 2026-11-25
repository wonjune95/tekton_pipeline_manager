import os

import cx_Oracle

# ok: mois-2-13-sensitive-comment-py 값이 아니라 자리표시자
# password: <운영팀에 문의>
# ok: mois-2-13-sensitive-comment-py 가린 값
# pwd = ********
# ok: mois-2-13-sensitive-comment-py 가린 값 뒤에 설명이 이어진다
# password: ******** (운영팀에 문의)
# ok: mois-2-13-sensitive-comment-py 값이 아니라 키·파라미터 이름을 설명한다
# 요청 JSON 의 password 키 이름은 "password"
# password 파라미터의 예전 이름은 "passwd"
# 설정 키 password 의 줄임 표기: "pwd"
# ok: mois-2-13-sensitive-comment-py 주석 처리한 코드 (값이 아니라 호출)
# password = get_secret("ora/password")
# ok: mois-2-13-sensitive-comment-py 정책 설명
# 비밀번호는 영문과 숫자를 섞어 만든다
# ok: mois-2-13-sensitive-comment-py 파일 경로
# 설정 파일: conf/admin/settings.py, 로그: /var/log/admin/app-2021.log


def connect():
    # ok: mois-2-13-sensitive-comment-py 문자열 안의 # 은 주석이 아니다
    banner = "password:#a1b2c3"
    dsn = os.environ["ORA_DSN"]  # DSN 형식: host:1521/service
    return cx_Oracle.connect(os.environ["ORA_USER"], os.environ["ORA_PASSWORD"], dsn), banner
