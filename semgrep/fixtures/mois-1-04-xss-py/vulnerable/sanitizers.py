"""이스케이프처럼 보이지만 출력에는 원래 값이 들어가는 경우 — 모두 탐지되어야 한다."""
import html

from django.http import HttpResponse
from django.utils.html import escape


def escape_result_discarded(request):
    keyword = request.GET.get("q", "")
    # 이스케이프한 결과를 쓰지 않음
    html.escape(keyword)
    # ruleid: mois-1-04-xss-py
    return HttpResponse("<p>검색어: " + keyword + "</p>")


def other_value_escaped(request):
    keyword = request.GET.get("q", "")
    category = request.GET.get("category", "")
    # 이스케이프한 값과 출력하는 값이 다르다
    safe_keyword = escape(keyword)
    # ruleid: mois-1-04-xss-py
    return HttpResponse("<p>" + safe_keyword + " / " + category + "</p>")


def html_content_type_stated(request):
    # HTML 이라고 명시한 응답은 제외 대상이 아니다
    # ruleid: mois-1-04-xss-py
    return HttpResponse("<p>" + request.GET.get("q", "") + "</p>", content_type="text/html")


def content_type_only_in_body_text(request):
    # 본문 글자에 content_type="..." 이 들어 있을 뿐, 응답은 HTML 이다
    # ruleid: mois-1-04-xss-py
    return HttpResponse("<pre>content_type='text/plain' 요청: " + request.GET.get("q", "") + "</pre>")
