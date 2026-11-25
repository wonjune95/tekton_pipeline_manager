# Django 비밀키를 소스에 적어 둠
# ruleid: mois-2-06-hardcoded-secret-py
SECRET_KEY = "django-insecure-4x!k2#p9v@1z"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "portal",
        "USER": "portal",
        # ruleid: mois-2-06-hardcoded-secret-py
        "PASSWORD": "Portal!2021",
        "HOST": "db.example.org",
    }
}

# ruleid: mois-2-06-hardcoded-secret-py
CELERY_BROKER_URL = "amqp://worker:w0rkerPass@mq.example.org:5672/portal"
