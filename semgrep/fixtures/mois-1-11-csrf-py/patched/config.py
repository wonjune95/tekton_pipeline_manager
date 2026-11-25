from flask import Flask
from flask_limiter import Limiter
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
limiter = Limiter(key_func=lambda: "global")


class ProductionConfig:
    # ok: mois-1-11-csrf-py CSRF 검사를 켠 설정
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600


def create_app():
    app = Flask(__name__)
    app.config.from_object(ProductionConfig)
    app.config.update(WTF_CSRF_ENABLED=True, WTF_CSRF_CHECK_DEFAULT=True)
    csrf.init_app(app)

    @app.route("/health")
    # ok: mois-1-11-csrf-py 요청 수 제한의 exempt 는 CSRF 와 무관하다
    @limiter.exempt
    def health():
        return {"ok": True}

    return app
