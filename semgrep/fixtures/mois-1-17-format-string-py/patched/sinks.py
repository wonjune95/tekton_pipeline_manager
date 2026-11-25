import logging

from django.http import JsonResponse

logger = logging.getLogger(__name__)


def padded(request):
    # ok: mois-1-17-format-string-py 형식에 들어가는 값은 정수·실수로 바꾼 값뿐이다
    width = int(request.GET.get("width", "10"))
    label = ("%" + str(width) + "s|") % "x"
    # "8.2" 같은 폭.정밀도 값은 실수로 바꿔 숫자만 남긴다
    spec = float(request.GET.get("spec", "8.2"))
    ratio = ("%" + str(spec) + "f") % 3.14159
    return JsonResponse({"label": label, "ratio": ratio})


def logged(request):
    action = request.POST.get("action", "")
    # ok: mois-1-17-format-string-py 인자가 없는 logging 호출은 메시지를 형식으로 해석하지 않는다
    logger.info("action=" + action)
    # ok: mois-1-17-format-string-py 형식은 상수, 입력은 인자
    logger.log(logging.INFO, "action=%s", action)
    # ok: mois-1-17-format-string-py
    return JsonResponse({"text": "{} 처리됨".format(action), "map": "{a}".format_map({"a": action})})
