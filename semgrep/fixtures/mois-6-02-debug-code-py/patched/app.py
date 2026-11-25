from flask import Flask

app = Flask(__name__)


@app.route("/ping")
def ping():
    return "pong"


# 개발용 서버 시작 블록은 디버그 코드가 아니다
if __name__ == "__main__":
    app.run()
