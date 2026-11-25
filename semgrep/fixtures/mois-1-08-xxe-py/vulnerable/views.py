from django.http import JsonResponse
from lxml import etree


def import_orders(request):
    # 기본 파서는 외부 엔티티를 해석함
    # ruleid: mois-1-08-xxe-py
    root = etree.fromstring(request.body)
    return JsonResponse({"count": len(root.findall("order"))})


def import_catalog(request):
    # resolve_entities 를 끄지 않은 파서
    # ruleid: mois-1-08-xxe-py
    parser = etree.XMLParser(load_dtd=True)
    tree = etree.parse(request.FILES["catalog"], parser)
    return JsonResponse({"root": tree.getroot().tag})
