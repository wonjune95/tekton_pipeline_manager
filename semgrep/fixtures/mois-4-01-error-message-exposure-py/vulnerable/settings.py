import os

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
# 운영 설정에 디버그 모드가 켜져 있어 오류 화면에 트레이스백·설정값이 노출됨
# ruleid: mois-4-01-error-message-exposure-py
DEBUG = True
ALLOWED_HOSTS = ["portal.example.go.kr"]
