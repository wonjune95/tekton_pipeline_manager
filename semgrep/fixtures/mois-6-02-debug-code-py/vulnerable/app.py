from flask import Flask

app = Flask(__name__)


@app.route("/ping")
def ping():
    # __main__ 블록이 있어도 웹 모듈의 print 는 디버그 출력이다
    # ruleid: mois-6-02-debug-code-py
    print("ping called")
    return "pong"


def _self_test():
    client = app.test_client()
    return client.get("/ping").status_code


# 웹 모듈에 남은 테스트용 실행 블록
# ruleid: mois-6-02-debug-code-py
if __name__ == "__main__":
    print("self test:", _self_test())
