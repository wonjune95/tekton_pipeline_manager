"""검증처럼 보이지만 검증이 아닌 경우 — 모두 탐지되어야 한다."""
import re

from django.http import HttpResponseBadRequest, JsonResponse
from lxml import etree

USERS_XML = "/srv/data/users.xml"
PARSER = etree.XMLParser(resolve_entities=False, no_network=True)
NAME_RE = re.compile(r"[A-Za-z0-9_]{1,40}")


def prefix_match_only(request):
    name = request.GET.get("name", "")
    # re.match 는 앞부분만 본다: "kim' or '1'='1" 도 통과
    if not re.match(r"[A-Za-z0-9_]+", name):
        return HttpResponseBadRequest("invalid name")
    tree = etree.parse(USERS_XML, PARSER)
    # ruleid: mois-1-09-xpath-injection-py
    nodes = tree.xpath("//user[@name='" + name + "']")
    return JsonResponse({"count": len(nodes)})


def compiled_prefix_match(request):
    name = request.GET.get("name", "")
    if not NAME_RE.match(name) or not NAME_RE.search(name):
        return HttpResponseBadRequest("invalid name")
    tree = etree.parse(USERS_XML, PARSER)
    # ruleid: mois-1-09-xpath-injection-py
    nodes = tree.xpath("//user[@name='" + name + "']")
    return JsonResponse({"count": len(nodes)})


def result_ignored(request):
    name = request.GET.get("name", "")
    # 검사 결과를 쓰지 않음
    NAME_RE.fullmatch(name)
    name.isalnum()
    tree = etree.parse(USERS_XML, PARSER)
    # ruleid: mois-1-09-xpath-injection-py
    nodes = tree.xpath("//user[@name='" + name + "']")
    return JsonResponse({"count": len(nodes)})


def failure_does_not_exit(request):
    name = request.GET.get("name", "")
    if not NAME_RE.fullmatch(name):
        print("suspicious name", name)
    tree = etree.parse(USERS_XML, PARSER)
    # ruleid: mois-1-09-xpath-injection-py
    nodes = tree.xpath("//user[@name='" + name + "']")
    return JsonResponse({"count": len(nodes)})


def opposite_branch(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if name.isalnum():
        nodes = []
    else:
        # ruleid: mois-1-09-xpath-injection-py
        nodes = tree.xpath("//user[@name='" + name + "']")
    return JsonResponse({"count": len(nodes)})


def used_when_check_fails(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    nodes = []
    if not re.fullmatch(r"[A-Za-z0-9_]+", name):
        # ruleid: mois-1-09-xpath-injection-py
        nodes = tree.xpath("//user[@name='" + name + "']")
    return JsonResponse({"count": len(nodes)})


def exits_when_check_passes(request):
    name = request.GET.get("name", "")
    # 조건이 반대: 형식이 맞으면 빠져나간다
    if NAME_RE.fullmatch(name):
        return HttpResponseBadRequest("reserved")
    tree = etree.parse(USERS_XML, PARSER)
    # ruleid: mois-1-09-xpath-injection-py
    nodes = tree.xpath("//user[@name='" + name + "']")
    return JsonResponse({"count": len(nodes)})


def other_variable_checked(request):
    name = request.GET.get("name", "")
    team = request.GET.get("team", "")
    if not name or not NAME_RE.fullmatch(name):
        return HttpResponseBadRequest("invalid name")
    tree = etree.parse(USERS_XML, PARSER)
    # 검사한 변수는 name 뿐이다
    # ruleid: mois-1-09-xpath-injection-py
    nodes = tree.xpath("//team[@id='" + team + "']/user[@name='" + name + "']")
    return JsonResponse({"count": len(nodes)})


def sink_inside_failing_branch(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if not NAME_RE.fullmatch(name):
        # 형식이 틀린 값으로 질의하고 빠져나간다
        # ruleid: mois-1-09-xpath-injection-py
        return JsonResponse({"count": len(tree.xpath("//user[@name='" + name + "']"))})
    return JsonResponse({"count": 0})


def nested_conditional_exit(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if not NAME_RE.fullmatch(name):
        if request.GET.get("strict"):
            return JsonResponse({"ok": True})
    # 엄격 모드가 아니면 검사에 실패한 값이 그대로 내려온다
    # ruleid: mois-1-09-xpath-injection-py
    tree.xpath("//user[@name='" + name + "']")
    return JsonResponse({"ok": True})


def reassigned_after_check(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if not NAME_RE.fullmatch(name):
        return JsonResponse({"ok": True})
    # 검사한 뒤에 다른 입력으로 바꿔 넣는다
    name = request.GET.get("alias", "")
    # ruleid: mois-1-09-xpath-injection-py
    tree.xpath("//user[@name='" + name + "']")
    return JsonResponse({"ok": True})


def appended_after_check(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if not NAME_RE.fullmatch(name):
        return JsonResponse({"ok": True})
    # 검사한 뒤에 검사하지 않은 입력을 덧붙인다
    name += request.GET.get("suffix", "")
    # ruleid: mois-1-09-xpath-injection-py
    tree.xpath("//user[@name='" + name + "']")
    return JsonResponse({"ok": True})


def check_joined_with_and(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    # 엄격 모드일 때만 검사한다
    if request.GET.get("strict") and not NAME_RE.fullmatch(name):
        return JsonResponse({"ok": True})
    # ruleid: mois-1-09-xpath-injection-py
    tree.xpath("//user[@name='" + name + "']")
    return JsonResponse({"ok": True})


def check_joined_with_or(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    # or 로 묶이면 검사를 통과하지 않은 값도 들어온다
    if request.user.is_staff or NAME_RE.fullmatch(name):
        # ruleid: mois-1-09-xpath-injection-py
        tree.xpath("//user[@name='" + name + "']")
    return JsonResponse({"ok": True})
