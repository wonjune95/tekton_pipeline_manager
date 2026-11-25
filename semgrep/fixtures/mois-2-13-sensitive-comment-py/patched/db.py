import os

import pymysql

# 접속 정보는 환경변수에서 읽는다. 비밀번호는 주석에 적지 않는다
# 비밀번호는 9자 이상이어야 한다 (정책: 영문+숫자+특수문자)
# password = os.environ["DB_PASSWORD"]
# pwd = hashlib.sha256(raw).hexdigest()
# see tests under test/test_db2.py and /home/user/app1/conf
NOTICE_COLOR = "color: #1a2b3c"


def connect():
    # 암호화된 채널로 접속
    return pymysql.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        ssl={"ca": os.environ["DB_CA_FILE"]},
    )
