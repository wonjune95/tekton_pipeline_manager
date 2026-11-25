"""guard 형태별 안전한 예제 (Django)."""
import re

from django.http import HttpResponse, HttpResponseBadRequest
from lxml import etree

USERS_XML = "/srv/data/users.xml"
PARSER = etree.XMLParser(resolve_entities=False, no_network=True)
NAME_RE = re.compile(r"[A-Za-z0-9_]{1,40}")


def guard_1(request):
    name = request.GET.get("name", "")
    if not re.fullmatch(r"[A-Za-z0-9_]{1,40}", name):
        return HttpResponseBadRequest("invalid")
    tree = etree.parse(USERS_XML, PARSER)
    # ok: mois-1-09-xpath-injection-py 실패하면 return
    tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def guard_2(request):
    name = request.GET.get("name", "")
    if not NAME_RE.fullmatch(name):
        raise ValueError("invalid")
    tree = etree.parse(USERS_XML, PARSER)
    # ok: mois-1-09-xpath-injection-py 실패하면 raise
    tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def guard_3(request):
    name = request.GET.get("name", "")
    if not name.isalnum():
        return HttpResponseBadRequest("invalid")
    tree = etree.parse(USERS_XML, PARSER)
    # ok: mois-1-09-xpath-injection-py 실패하면 return
    tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def guard_4(request):
    name = request.GET.get("name", "")
    if not name or not re.fullmatch(r"[A-Za-z0-9_]{1,40}", name):
        raise ValueError("invalid")
    tree = etree.parse(USERS_XML, PARSER)
    # ok: mois-1-09-xpath-injection-py 값이 없거나 실패하면 raise
    tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def guard_5(request):
    name = request.GET.get("name", "")
    if not name or not NAME_RE.fullmatch(name):
        return HttpResponseBadRequest("invalid")
    tree = etree.parse(USERS_XML, PARSER)
    # ok: mois-1-09-xpath-injection-py 값이 없거나 실패하면 return
    tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def guard_6(request):
    name = request.GET.get("name", "")
    if not name or not name.isalnum():
        raise ValueError("invalid")
    tree = etree.parse(USERS_XML, PARSER)
    # ok: mois-1-09-xpath-injection-py 값이 없거나 실패하면 raise
    tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def guard_7(request):
    for name in request.GET.getlist("name"):
        if not re.fullmatch(r"[A-Za-z0-9_]{1,40}", name):
            continue
        tree = etree.parse(USERS_XML, PARSER)
        # ok: mois-1-09-xpath-injection-py 실패한 값은 건너뜀
        tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def guard_8(request):
    for name in request.GET.getlist("name"):
        if not name or not name.isalnum():
            continue
        tree = etree.parse(USERS_XML, PARSER)
        # ok: mois-1-09-xpath-injection-py 비었거나 실패한 값은 건너뜀
        tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def guard_9(request):
    name = request.GET.get("name", "")
    if re.fullmatch(r"[A-Za-z0-9_]{1,40}", name):
        tree = etree.parse(USERS_XML, PARSER)
        # ok: mois-1-09-xpath-injection-py 검사를 통과한 조건 안에서만 사용
        tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def guard_10(request):
    name = request.GET.get("name", "")
    if NAME_RE.fullmatch(name):
        tree = etree.parse(USERS_XML, PARSER)
        # ok: mois-1-09-xpath-injection-py 검사를 통과한 조건 안에서만 사용
        tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def guard_11(request):
    name = request.GET.get("name", "")
    if name.isalnum():
        tree = etree.parse(USERS_XML, PARSER)
        # ok: mois-1-09-xpath-injection-py 검사를 통과한 조건 안에서만 사용
        tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")
