# ruleid: mois-6-02-debug-code-py
import pdb  # 디버거 import 가 남아 있음
import sys

from django.http import JsonResponse

from .models import Order


def order_detail(request, order_id):
    order = Order.objects.get(pk=order_id)
    # ruleid: mois-6-02-debug-code-py
    print("order loaded:", order.id, order.buyer_email)  # 디버그 출력
    # ruleid: mois-6-02-debug-code-py
    pdb.set_trace()  # 디버거 중단점
    return JsonResponse({"id": order.id})


def order_list(request):
    orders = Order.objects.filter(buyer=request.user)
    # ruleid: mois-6-02-debug-code-py
    print(f"count={orders.count()}", file=sys.stderr)  # 디버그 출력
    # ruleid: mois-6-02-debug-code-py
    breakpoint()  # 디버거 중단점
    return JsonResponse({"count": orders.count()})
