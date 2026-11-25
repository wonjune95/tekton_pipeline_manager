import json

import yaml
from django.http import JsonResponse


def restore_cart(request):
    # 데이터만 담는 형식(JSON)으로 읽고 형식을 확인
    try:
        cart = json.loads(request.COOKIES.get("cart", "[]"))
    except ValueError:
        return JsonResponse({"error": "E400"}, status=400)
    if not isinstance(cart, list):
        return JsonResponse({"error": "E400"}, status=400)
    return JsonResponse({"items": len(cart)})


def import_config(request):
    config = yaml.safe_load(request.body) or {}
    return JsonResponse({"keys": list(config)})


def import_rules(request):
    rules = yaml.load(request.body, Loader=yaml.SafeLoader) or {}
    return JsonResponse({"count": len(rules)})
