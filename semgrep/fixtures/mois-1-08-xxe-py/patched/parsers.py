import xml.etree.ElementTree as ET

import defusedxml.ElementTree as SafeET
import xmltodict
from django.http import JsonResponse
from lxml import etree, objectify

SAFE_PARSER = etree.XMLParser(resolve_entities=False, no_network=True)
SCHEMA = etree.fromstring("<schema version='1'/>")


def explicit_safe_parser(request):
    # ok: mois-1-08-xxe-py resolve_entities=False 로 만든 파서를 넘겨 읽는다
    parser = etree.XMLParser(resolve_entities=False)
    a = etree.fromstring(request.body, parser)
    b = etree.XML(request.body, parser=parser)
    c = objectify.fromstring(request.body, SAFE_PARSER)
    d = etree.parse(request.FILES["doc"], parser=SAFE_PARSER)
    e = objectify.parse(request.FILES["doc"], SAFE_PARSER)
    return JsonResponse({"tags": [a.tag, b.tag, c.tag, d.getroot().tag, e.getroot().tag]})


def incremental(request):
    # ok: mois-1-08-xxe-py
    events = [el.tag for _, el in etree.iterparse(request.FILES["feed"], resolve_entities=False)]
    pull = etree.XMLPullParser(events=("start",), resolve_entities=False)
    pull.feed(request.body)
    return JsonResponse({"events": events, "pulled": len(list(pull.read_events()))})


def fixed_documents(request):
    # ok: mois-1-08-xxe-py 고정 문자열·고정 파일은 외부 입력이 아니다
    template = etree.XML("<reply><status/></reply>")
    layout = etree.parse("/srv/app/layout.xml")
    return JsonResponse({"tags": [template.tag, layout.getroot().tag, SCHEMA.tag]})


def other_libraries(request):
    # ok: mois-1-08-xxe-py 표준 라이브러리 ElementTree 와 defusedxml 은 외부 엔티티를 읽지 않는다
    a = ET.fromstring(request.body)
    b = SafeET.fromstring(request.body)
    # ok: mois-1-08-xxe-py xmltodict 기본값은 엔티티를 풀지 않는다
    c = xmltodict.parse(request.body)
    return JsonResponse({"tags": [a.tag, b.tag], "doc": c})
