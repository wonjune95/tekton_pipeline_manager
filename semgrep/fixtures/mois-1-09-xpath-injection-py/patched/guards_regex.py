"""형식 검사 guard 의 안전한 예제 — 허용 문자만 적은 정규식 리터럴과 and 로 묶은 조건."""
import re

from django.http import HttpResponse, HttpResponseBadRequest
from lxml import etree

USERS_XML = "/srv/data/users.xml"
PARSER = etree.XMLParser(resolve_entities=False, no_network=True)
GOOD_RE = re.compile(r"[A-Za-z0-9_]{1,40}")
DIGITS_RE = re.compile(r"\d{1,9}")


def digits_inline(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if not re.fullmatch(r"\d{1,9}", name):
        return HttpResponseBadRequest("invalid")
    # ok: mois-1-09-xpath-injection-py \d 만 적은 정규식 (실패하면 return)
    tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def digits_compiled(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if not DIGITS_RE.fullmatch(name):
        return HttpResponseBadRequest("invalid")
    # ok: mois-1-09-xpath-injection-py 모듈 수준에서 컴파일한 \d 정규식 (실패하면 return)
    tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def digits_inline_inside_if(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if re.fullmatch(r"\d{1,9}", name):
        # ok: mois-1-09-xpath-injection-py \d 만 적은 정규식을 통과한 조건 안
        tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def digits_compiled_inside_if(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if DIGITS_RE.fullmatch(name):
        # ok: mois-1-09-xpath-injection-py 컴파일한 \d 정규식을 통과한 조건 안
        tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def nonempty_and_ischeck(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if name and name.isalnum():
        # ok: mois-1-09-xpath-injection-py 값이 있고(and) 검사를 통과한 조건 안
        tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def nonempty_and_compiled(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if name and GOOD_RE.fullmatch(name):
        # ok: mois-1-09-xpath-injection-py 값이 있고(and) 컴파일한 정규식을 통과한 조건 안
        tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def nonempty_and_inline(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if name and re.fullmatch(r"[A-Za-z0-9_]{1,40}", name):
        # ok: mois-1-09-xpath-injection-py 값이 있고(and) 조건에 적은 정규식을 통과한 조건 안
        tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def literal_tokens(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if not re.fullmatch(r"(?:[a-z0-9]+-)*[a-z0-9]+@[\w-]+\.example\.com", name, re.IGNORECASE):
        return HttpResponseBadRequest("invalid")
    # ok: mois-1-09-xpath-injection-py 글자·묶음·\w·\. 만 쓴 정규식
    tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")
