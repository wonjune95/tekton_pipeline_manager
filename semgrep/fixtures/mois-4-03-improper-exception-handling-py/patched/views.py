import logging

from django.http import JsonResponse

from .services import PaymentDeclined, PaymentGatewayError, charge, refund

logger = logging.getLogger(__name__)


def pay(request, order_id):
    try:
        receipt = charge(order_id, request.POST.get("quantity", "1"))
    except PaymentDeclined:
        # 예상되는 예외는 종류별로 나눠 처리
        return JsonResponse({"ok": False, "error": "E402"}, status=402)
    except PaymentGatewayError:
        logger.exception("payment gateway error: order=%s", order_id)
        return JsonResponse({"ok": False, "error": "E502"}, status=502)
    return JsonResponse({"ok": True, "receipt": receipt.id})


def cancel(request, order_id):
    try:
        refund(order_id)
    except Exception:
        # 모두 잡아야 할 때는 기록한 뒤 다시 던진다
        logger.exception("refund failed: order=%s", order_id)

        if order_id:
            raise
        raise
    return JsonResponse({"ok": True})


def status(request, order_id):
    try:
        state = charge.status(order_id)
    except ValueError:
        state = "unknown"
    return JsonResponse({"state": state})
