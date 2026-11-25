import logging

from django.http import HttpResponse, JsonResponse

from .services import load_member

logger = logging.getLogger(__name__)


def member_detail(request, member_id):
    try:
        member = load_member(member_id)
    except LookupError:
        # 상세 내용은 로그로만 남기고 사용자에게는 정해진 코드만 준다
        logger.warning("member not found: %s", member_id)
        return JsonResponse({"error": "E404"}, status=404)
    return JsonResponse({"name": member.name})


def member_export(request, member_id):
    try:
        data = load_member(member_id).export()
    except ValueError:
        logger.exception("member export failed")
        return HttpResponse("E500", status=500)
    return JsonResponse({"data": data})
