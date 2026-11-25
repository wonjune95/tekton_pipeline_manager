from django.http import JsonResponse
from lxml import etree

USERS_XML = "/srv/data/users.xml"
PARSER = etree.XMLParser(resolve_entities=False, no_network=True)


def find_user(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    # 외부 입력을 XPath 질의문에 이어 붙임
    # ruleid: mois-1-09-xpath-injection-py
    nodes = tree.xpath("//user[@name='" + name + "']/email/text()")
    return JsonResponse({"emails": [str(node) for node in nodes]})
