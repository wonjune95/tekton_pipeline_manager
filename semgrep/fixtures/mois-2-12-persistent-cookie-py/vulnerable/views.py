from datetime import datetime, timedelta, timezone

from django.http import JsonResponse


def remember_member(request):
    response = JsonResponse({"result": "ok"})
    # 1년 동안 디스크에 남는 쿠키
    # ruleid: mois-2-12-persistent-cookie-py
    response.set_cookie("member_id", request.user.get_username(), max_age=60 * 60 * 24 * 365, secure=True, httponly=True)
    return response


def keep_login(request):
    response = JsonResponse({"result": "ok"})
    # ruleid: mois-2-12-persistent-cookie-py
    response.set_cookie("auto_login", "1", expires=datetime.now(timezone.utc) + timedelta(days=30), secure=True, httponly=True)
    # ruleid: mois-2-12-persistent-cookie-py
    request.session.set_expiry(2592000)
    return response
