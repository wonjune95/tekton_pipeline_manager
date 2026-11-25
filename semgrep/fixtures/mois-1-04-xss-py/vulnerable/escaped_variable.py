"""이스케이프한 값을 변수에 담았다가 HTML 이스케이프가 막지 못하는 위치에 넣는 경우 — 모두 탐지되어야 한다."""
import html

from django.http import HttpResponse


def link_by_concat(request):
    safe = html.escape(request.GET["next"])
    # href 맨 앞이면 javascript:alert(1) 이 그대로 남는다
    # ruleid: mois-1-04-xss-py
    return HttpResponse('<a href="' + safe + '">go</a>')


def image_src(request):
    safe = html.escape(request.GET["img"])
    # ruleid: mois-1-04-xss-py
    return HttpResponse('<img src="' + safe + '">')


def form_action(request):
    safe = html.escape(request.GET["to"])
    # ruleid: mois-1-04-xss-py
    return HttpResponse("<form action='" + safe + "'></form>")


def script_by_percent(request):
    safe = html.escape(request.GET["q"])
    body = "<script>var q = '%s';</script>" % safe
    # ruleid: mois-1-04-xss-py
    return HttpResponse(body)


def link_by_format(request):
    safe = html.escape(request.GET["next"])
    # ruleid: mois-1-04-xss-py
    return HttpResponse('<a href="{}">go</a>'.format(safe))


def event_handler(request):
    safe = html.escape(request.GET["name"])
    # 속성 값 안의 엔티티는 풀린 뒤 스크립트로 실행된다
    # ruleid: mois-1-04-xss-py
    return HttpResponse('<button onclick="greet(\'' + safe + '\')">hi</button>')


def javascript_url(request):
    safe = html.escape(request.GET["id"])
    # ruleid: mois-1-04-xss-py
    return HttpResponse("<span data-go='javascript:open(" + safe + ")'>go</span>")


def unquoted_attribute(request):
    safe = html.escape(request.GET["v"])
    # 따옴표 없는 속성 값은 공백 하나로 새 속성을 시작할 수 있다
    # ruleid: mois-1-04-xss-py
    return HttpResponse("<input value=" + safe + ">")


def unquoted_attribute_percent(request):
    safe = html.escape(request.GET["v"])
    # ruleid: mois-1-04-xss-py
    return HttpResponse("<input value=%s>" % safe)


def unquoted_attribute_format(request):
    safe = html.escape(request.GET["v"])
    # ruleid: mois-1-04-xss-py
    return HttpResponse("<input value={}>".format(safe))
