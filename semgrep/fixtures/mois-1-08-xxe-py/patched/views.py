from django.http import JsonResponse
from lxml import etree


def import_orders(request):
    # ok: mois-1-08-xxe-py 외부 엔티티·네트워크 접근을 막은 파서를 지정
    parser = etree.XMLParser(resolve_entities=False, no_network=True)
    root = etree.fromstring(request.body, parser)
    return JsonResponse({"count": len(root.findall("order"))})


def import_catalog(request):
    parser = etree.XMLParser(resolve_entities=False, no_network=True)
    tree = etree.parse(request.FILES["catalog"], parser)
    return JsonResponse({"root": tree.getroot().tag})
