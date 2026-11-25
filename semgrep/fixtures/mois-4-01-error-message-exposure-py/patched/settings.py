import os

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
# 운영에서는 꺼져 있고, 개발 환경에서만 환경변수로 켠다
DEBUG = os.environ.get("DJANGO_DEBUG", "") == "1"
ALLOWED_HOSTS = ["portal.example.go.kr"]
