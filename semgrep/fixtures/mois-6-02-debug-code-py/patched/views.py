import logging

from django.http import JsonResponse

from .models import Order

logger = logging.getLogger(__name__)


def order_detail(request, order_id):
    order = Order.objects.get(pk=order_id)
    logger.debug("order loaded: %s", order.id)
    return JsonResponse({"id": order.id})


def order_list(request):
    orders = Order.objects.filter(buyer=request.user)
    return JsonResponse({"count": orders.count()})
