from django.http import HttpResponse
from django.shortcuts import render
from django.utils.html import escape, format_html


def search(request):
    keyword = request.GET.get("q", "")
    # ok: mois-1-04-xss-py HTML 특수문자를 이스케이프해 출력
    return HttpResponse("<p>검색어: " + escape(keyword) + "</p>")


def nickname_badge(request):
    nickname = request.POST.get("nickname", "")
    # ok: mois-1-04-xss-py format_html 은 인자를 이스케이프함
    badge = format_html("<b>{}</b>", nickname)
    return render(request, "profile.html", {"badge": badge})
