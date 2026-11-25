from flask import Flask


class DevelopmentConfig:
    # 설정 클래스·모듈에서 전역으로 끔
    # ruleid: mois-1-11-csrf-py
    WTF_CSRF_ENABLED = False


class ApiConfig:
    # 기본 검사를 끄고 뷰마다 직접 호출하도록 바꿈 (호출을 빠뜨리면 보호되지 않는다)
    # ruleid: mois-1-11-csrf-py
    WTF_CSRF_CHECK_DEFAULT = False


def create_app():
    app = Flask(__name__)
    # ruleid: mois-1-11-csrf-py
    app.config["WTF_CSRF_CHECK_DEFAULT"] = False
    # ruleid: mois-1-11-csrf-py
    app.config.update(SECRET_KEY="dev", WTF_CSRF_ENABLED=False)
    # ruleid: mois-1-11-csrf-py
    app.config.update(WTF_CSRF_CHECK_DEFAULT=False)
    return app
