import os

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "portal",
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": "db.example.org",
    }
}

CELERY_BROKER_URL = os.environ["CELERY_BROKER_URL"]

# 값이 아니라 필드·헤더 이름
PASSWORD_FIELD = "password"
CSRF_COOKIE_NAME = "csrftoken"
AUTH_HEADER_TOKEN = "Authorization"
TOKEN_URL = "/api/auth/token"
DEFAULT_PASSWORD = ""
