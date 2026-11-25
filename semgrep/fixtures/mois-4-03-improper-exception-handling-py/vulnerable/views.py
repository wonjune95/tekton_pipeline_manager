import logging

from django.http import JsonResponse

from .services import charge, refund

logger = logging.getLogger(__name__)


def pay(request, order_id):
    try:
        receipt = charge(order_id, request.POST.get("quantity", "1"))
    # ruleid: mois-4-03-improper-exception-handling-py
    except Exception as e:  # 모든 예외를 한꺼번에 잡고 실패를 숨김
        logger.error("charge failed: %s", e)
        return JsonResponse({"ok": False})
    return JsonResponse({"ok": True, "receipt": receipt.id})


def cancel(request, order_id):
    try:
        refund(order_id)
    # ruleid: mois-4-03-improper-exception-handling-py
    except:  # 예외 종류를 지정하지 않음 (KeyboardInterrupt·SystemExit 까지 잡힘)
        logger.error("refund failed")

        return JsonResponse({"ok": False})
    return JsonResponse({"ok": True})


def status(request, order_id):
    try:
        state = charge.status(order_id)
    # ruleid: mois-4-03-improper-exception-handling-py
    except (ValueError, BaseException):  # 광범위한 예외
        state = "unknown"
    return JsonResponse({"state": state})
