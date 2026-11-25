from django.http import JsonResponse


def remember_member(request):
    response = JsonResponse({"result": "ok"})
    # 하루만 유지하고 중요정보는 넣지 않는다
    response.set_cookie("recent_menu", "notice", max_age=60 * 60 * 24, secure=True, httponly=True, samesite="Lax")
    return response


def keep_login(request):
    response = JsonResponse({"result": "ok"})
    # 만료를 지정하지 않으면 브라우저를 닫을 때 지워진다
    response.set_cookie("layout", "wide", secure=True, httponly=True, samesite="Lax")
    request.session.set_expiry(0)
    return response
