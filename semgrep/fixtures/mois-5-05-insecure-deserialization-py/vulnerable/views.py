import base64
import pickle

import yaml
from django.http import JsonResponse


def restore_cart(request):
    # 쿠키 값을 그대로 pickle 로 역직렬화: 임의 코드 실행
    # ruleid: mois-5-05-insecure-deserialization-py
    cart = pickle.loads(base64.b64decode(request.COOKIES["cart"]))
    return JsonResponse({"items": len(cart)})


def import_config(request):
    # ruleid: mois-5-05-insecure-deserialization-py
    config = yaml.load(request.body, Loader=yaml.Loader)  # 임의 객체를 만드는 Loader
    return JsonResponse({"keys": list(config)})


def upload_model(request):
    # ruleid: mois-5-05-insecure-deserialization-py
    model = pickle.load(request.FILES["model"])  # 업로드 파일을 pickle 로 읽음
    return JsonResponse({"name": model.name})
