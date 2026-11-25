from django.http import JsonResponse
from lxml import etree

USERS_XML = "/srv/data/users.xml"
PARSER = etree.XMLParser(resolve_entities=False, no_network=True)


def find_user(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    # ok: mois-1-09-xpath-injection-py 값은 XPath 변수로 전달
    nodes = tree.xpath("//user[@name=$name]/email/text()", name=name)
    return JsonResponse({"emails": [str(node) for node in nodes]})
