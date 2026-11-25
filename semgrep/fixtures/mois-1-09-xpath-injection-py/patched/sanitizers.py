import xml.etree.ElementTree as ET

from django.http import JsonResponse
from lxml import etree

USERS_XML = "/srv/data/users.xml"
PARSER = etree.XMLParser(resolve_entities=False, no_network=True)
FIND_BY_NAME = etree.XPath("//user[@name=$name]")


def numeric_position(request):
    tree = etree.parse(USERS_XML, PARSER)
    # ok: mois-1-09-xpath-injection-py 정수로 바꾼 값
    nodes = tree.xpath("//user[%d]" % int(request.GET.get("pos", "1")))
    return JsonResponse({"count": len(nodes)})


def compiled_with_variable(request):
    tree = etree.parse(USERS_XML, PARSER)
    # ok: mois-1-09-xpath-injection-py 컴파일한 질의문에 XPath 변수로 값을 넘김
    nodes = FIND_BY_NAME(tree, name=request.GET.get("name", ""))
    return JsonResponse({"count": len(nodes)})


def string_search(request):
    host = request.GET.get("host", "")
    page = request.POST.get("page", "")
    # ok: mois-1-09-xpath-injection-py str.find·str.count 는 XPath 가 아니다 ("http://" 의 // 는 경로식이 아님)
    pos = page.find("http://" + host)
    words = page.find(host)
    return JsonResponse({"pos": pos, "words": words})


def fixed_path(request):
    root = ET.parse(USERS_XML).getroot()
    wanted = request.GET.get("name", "")
    # ok: mois-1-09-xpath-injection-py 경로식은 고정하고 값은 Python 에서 비교
    names = [u.findtext("name") for u in root.findall(".//user") if u.findtext("name") == wanted]
    return JsonResponse({"names": names})
