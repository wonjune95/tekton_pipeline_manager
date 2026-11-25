from django.http import HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe


def search(request):
    keyword = request.GET.get("q", "")
    # 외부 입력을 이스케이프 없이 HTML 응답에 출력
    # ruleid: mois-1-04-xss-py
    return HttpResponse("<p>검색어: " + keyword + "</p>")


def nickname_badge(request):
    nickname = request.POST.get("nickname", "")
    # 외부 입력을 안전한 HTML 로 표시해 템플릿 자동 이스케이프를 끔
    # ruleid: mois-1-04-xss-py
    badge = mark_safe("<b>%s</b>" % nickname)
    return render(request, "profile.html", {"badge": badge})
