import logging

from django.http import JsonResponse

logger = logging.getLogger(__name__)

NOTICE_TEMPLATES = {
    "hello": "{name} 님 안녕하세요",
    "bye": "{name} 님 안녕히 가세요",
}


def render_notice(request):
    # 형식 문자열은 서버가 가진 것만 사용하고, 입력은 인자로 전달
    template = NOTICE_TEMPLATES.get(request.GET.get("template", "hello"))
    if template is None:
        template = NOTICE_TEMPLATES["hello"]
    # ok: mois-1-17-format-string-py 같은 파일의 dict 에서 꺼낸 형식 문자열
    message = template.format(name=request.user.get_username())
    return JsonResponse({"message": message})


def audit(request):
    action = request.POST.get("action", "")
    # ok: mois-1-17-format-string-py 형식은 상수, 입력은 인자
    logger.info("action=%s user=%s", action, request.user.pk)
    return JsonResponse({"ok": True})
