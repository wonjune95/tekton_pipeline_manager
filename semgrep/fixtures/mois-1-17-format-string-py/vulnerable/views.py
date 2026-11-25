import logging

from django.conf import settings
from django.http import JsonResponse

logger = logging.getLogger(__name__)


def render_notice(request):
    template = request.GET.get("template", "{user} 님 안녕하세요")
    # 외부 입력을 형식 문자열로 사용 ({user.__class__} 같은 필드로 내부 객체 접근 가능)
    # ruleid: mois-1-17-format-string-py
    message = template.format(user=request.user, site=settings)
    return JsonResponse({"message": message})


def audit(request):
    action = request.POST.get("action", "")
    # 외부 입력이 들어간 문자열을 logging 형식 문자열로 사용
    # ruleid: mois-1-17-format-string-py
    logger.info("action=" + action + " user=%s", request.user.pk)
    return JsonResponse({"ok": True})
