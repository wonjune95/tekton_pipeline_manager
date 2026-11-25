import os

# 인수인계용으로 남긴 주석에 계정·비밀번호가 그대로 있다 (표현별)

# 값에 숫자·특수문자가 있는 경우 (따옴표 없음)
# ruleid: mois-2-13-sensitive-comment-py
# default password is admin1234
# ruleid: mois-2-13-sensitive-comment-py
# 임시 passwd = Temp#2023
# ruleid: mois-2-13-sensitive-comment-py
# 비밀번호 초기값은 init#01
FTP_HOST = os.environ["FTP_HOST"]

# 값을 따옴표로 감싼 경우 (숫자·특수문자 없음)
# ruleid: mois-2-13-sensitive-comment-py
# 관리자 pwd = 'admin' 초기값 그대로
# ruleid: mois-2-13-sensitive-comment-py
# 관리자 비밀번호: "qwerty"
# ruleid: mois-2-13-sensitive-comment-py
# 패스워드는 "welcome"
# ruleid: mois-2-13-sensitive-comment-py
# 접속 암호 값은 'guest'
KIOSK_ID = os.environ["KIOSK_ID"]

# 계정 / 비밀번호 쌍, 빗금 양쪽에 공백 (DB·서버의 흔한 계정 이름)
# ruleid: mois-2-13-sensitive-comment-py
# 관리 콘솔 admin / admin123
# ruleid: mois-2-13-sensitive-comment-py
# 윈도 서버 administrator / Win#2019
# ruleid: mois-2-13-sensitive-comment-py
# MSSQL 접속 sa / P@ssw0rd
# ruleid: mois-2-13-sensitive-comment-py
# Oracle 관리 계정 sys / oracle12 as sysdba
# ruleid: mois-2-13-sensitive-comment-py
# 설치 직후 계정 system / manager1 그대로 사용 중
# ruleid: mois-2-13-sensitive-comment-py
# 시험 서버 test / test1234
# ruleid: mois-2-13-sensitive-comment-py
# 파일 서버 user / ftp#2020
CONSOLE_URL = os.environ["CONSOLE_URL"]

# 계정/비밀번호 쌍, 공백 없음 (관리자 계정 이름만)
# ruleid: mois-2-13-sensitive-comment-py
# 개발 DB 계정 root/Dev#2022
# ruleid: mois-2-13-sensitive-comment-py
# 원격 데스크톱 administrator/Win2019! 로 접속
# ruleid: mois-2-13-sensitive-comment-py
# 실습용 Oracle 계정 scott/tiger1
ORACLE_SID = os.environ["ORACLE_SID"]
