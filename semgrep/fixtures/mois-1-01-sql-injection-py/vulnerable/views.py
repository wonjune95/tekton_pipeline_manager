from django.db import connection
from django.http import JsonResponse

from .models import Member


def member_list(request):
    name = request.GET.get("name", "")
    with connection.cursor() as cursor:
        # 외부 입력을 질의문에 직접 이어 붙임
        # ruleid: mois-1-01-sql-injection-py
        cursor.execute("SELECT id, name FROM member WHERE name = '" + name + "'")
        rows = cursor.fetchall()
    return JsonResponse({"rows": rows})


def member_search(request):
    keyword = request.POST["keyword"]
    # ruleid: mois-1-01-sql-injection-py
    members = Member.objects.raw("SELECT * FROM member WHERE name LIKE '%%%s%%'" % keyword)
    return JsonResponse({"count": len(list(members))})
