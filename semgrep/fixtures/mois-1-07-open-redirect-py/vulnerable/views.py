from django.http import HttpResponseRedirect
from django.shortcuts import redirect


def after_login(request):
    next_url = request.GET.get("next", "/")
    # 이동할 주소를 외부 입력 그대로 사용
    # ruleid: mois-1-07-open-redirect-py
    return redirect(next_url)


def outbound(request):
    # ruleid: mois-1-07-open-redirect-py
    return HttpResponseRedirect(request.GET["url"])
