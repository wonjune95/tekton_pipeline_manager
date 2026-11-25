import traceback

from django.http import HttpResponse, JsonResponse

from .services import load_member


def member_detail(request, member_id):
    try:
        member = load_member(member_id)
    except LookupError as e:
        # 예외 메시지를 그대로 응답에 넣음
        # ruleid: mois-4-01-error-message-exposure-py
        return JsonResponse({"error": str(e)}, status=404)
    return JsonResponse({"name": member.name})


def member_export(request, member_id):
    try:
        data = load_member(member_id).export()
    except ValueError:
        # ruleid: mois-4-01-error-message-exposure-py
        traceback.print_exc()  # 트레이스백을 콘솔에 출력
        # ruleid: mois-4-01-error-message-exposure-py
        return HttpResponse(traceback.format_exc(), status=500)  # 트레이스백을 응답으로 반환
    return JsonResponse({"data": data})
