import os
import re

from django.http import JsonResponse

from .models import Member

ORDER_NO = re.compile(r"^ORD-(\d+)$")


def order_number(request):
    m = re.match(r"^ORD-(\d+)$", request.GET.get("no", ""))
    if m is None:
        return JsonResponse({"error": "E400"}, status=400)
    return JsonResponse({"number": m.group(1)})


def search(request):
    keyword = request.GET.get("q", "").strip()
    member = Member.objects.filter(name=keyword).first()
    if not member:
        return JsonResponse({"error": "E404"}, status=404)
    return JsonResponse({"email": member.email})


def first_reviewer(request):
    admin = Member.objects.filter(is_reviewer=True).first()
    name = admin.name if admin else ""
    hosts = os.environ.get("ALLOWED_PEERS", "").split(",")
    return JsonResponse({"name": name, "hosts": hosts})


def parse(request):
    m = ORDER_NO.search(request.POST.get("no", ""))
    return JsonResponse({"number": m.group(1) if m else None})


def member_name(request, member_id):
    # objects.get() 은 없으면 예외를 던지므로 None 이 아니다
    return JsonResponse({"name": Member.objects.get(pk=member_id).name})
