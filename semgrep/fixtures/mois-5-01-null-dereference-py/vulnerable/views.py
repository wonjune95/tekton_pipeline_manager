import os
import re

from django.http import JsonResponse

from .models import Member

ORDER_NO = re.compile(r"^ORD-(\d+)$")


def order_number(request):
    # 형식이 맞지 않으면 match() 가 None 을 돌려줌
    # ruleid: mois-5-01-null-dereference-py
    number = re.match(r"^ORD-(\d+)$", request.GET.get("no", "")).group(1)
    return JsonResponse({"number": number})


def search(request):
    # ruleid: mois-5-01-null-dereference-py
    keyword = request.GET.get("q").strip()  # 파라미터가 없으면 None
    member = Member.objects.filter(name=keyword).first()
    # ruleid: mois-5-01-null-dereference-py
    return JsonResponse({"email": member.email})  # 조회 결과가 없으면 None


def first_reviewer(request):
    # ruleid: mois-5-01-null-dereference-py
    name = Member.objects.filter(is_reviewer=True).first().name  # 결과가 없으면 None
    # ruleid: mois-5-01-null-dereference-py
    hosts = os.environ.get("ALLOWED_PEERS").split(",")  # 환경변수가 없으면 None
    return JsonResponse({"name": name, "hosts": hosts})


def parse(request):
    m = ORDER_NO.search(request.POST.get("no", ""))
    # ruleid: mois-5-01-null-dereference-py
    return JsonResponse({"number": m.group(1)})
