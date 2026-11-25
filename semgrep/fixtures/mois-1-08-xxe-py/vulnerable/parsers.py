import xml.sax
from xml.sax.handler import feature_external_pes

import xmltodict
from django.http import JsonResponse
from lxml import etree, objectify


def parser_options(request):
    # resolve_entities 를 명시하지 않았거나 켠 파서
    # ruleid: mois-1-08-xxe-py
    default_parser = etree.XMLParser()
    # ruleid: mois-1-08-xxe-py
    explicit = etree.XMLParser(resolve_entities=True, no_network=True)
    root = etree.fromstring(request.body, default_parser)
    other = etree.fromstring(request.body, parser=explicit)
    return JsonResponse({"tags": [root.tag, other.tag]})


def safe_and_unsafe_side_by_side(request):
    safe = etree.XMLParser(resolve_entities=False, no_network=True)
    # 같은 함수에 안전한 파서가 있어도, 이 파서는 따로 판정한다
    # ruleid: mois-1-08-xxe-py
    lenient = etree.XMLParser(recover=True)
    header = etree.fromstring(request.POST["header"], safe)
    body = etree.fromstring(request.body, lenient)
    return JsonResponse({"tags": [header.tag, body.tag]})


def incremental(request):
    # ruleid: mois-1-08-xxe-py
    events = [el.tag for _, el in etree.iterparse(request.FILES["feed"])]
    # ruleid: mois-1-08-xxe-py
    pull = etree.XMLPullParser(events=("start",))
    pull.feed(request.body)
    return JsonResponse({"events": events, "pulled": len(list(pull.read_events()))})


def default_parser_calls(request):
    data = request.body
    # 파서를 지정하지 않으면 기본 파서가 쓰인다
    # ruleid: mois-1-08-xxe-py
    a = etree.XML(data)
    # ruleid: mois-1-08-xxe-py
    b = etree.parse(request.FILES["doc"])
    # ruleid: mois-1-08-xxe-py
    c = objectify.fromstring(data)
    # ruleid: mois-1-08-xxe-py
    d = objectify.parse(request.FILES["doc"])
    # 파서가 아닌 인자(base_url)만 더 준 경우
    # ruleid: mois-1-08-xxe-py
    e = etree.fromstring(data, base_url="https://schemas.example.go.kr/")
    return JsonResponse({"tags": [a.tag, b.getroot().tag, c.tag, d.getroot().tag, e.tag]})


def sax_parameter_entities(request, handler):
    parser = xml.sax.make_parser()
    # 외부 파라미터 엔티티 처리를 켬
    # ruleid: mois-1-08-xxe-py
    parser.setFeature(feature_external_pes, True)
    parser.setContentHandler(handler)
    parser.feed(request.body)
    return JsonResponse({"ok": True})


def dict_conversion(request):
    # ruleid: mois-1-08-xxe-py
    doc = xmltodict.parse(request.body, disable_entities=False)
    return JsonResponse(doc)
