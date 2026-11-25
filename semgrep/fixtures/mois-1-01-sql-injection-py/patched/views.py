from django.db import connection
from django.http import JsonResponse

from .models import Member


def member_list(request):
    name = request.GET.get("name", "")
    with connection.cursor() as cursor:
        # ok: mois-1-01-sql-injection-py 값은 바인딩 매개변수로 전달
        cursor.execute("SELECT id, name FROM member WHERE name = %s", [name])
        rows = cursor.fetchall()
    return JsonResponse({"rows": rows})


def member_search(request):
    keyword = request.POST.get("keyword", "")
    # ok: mois-1-01-sql-injection-py ORM 필터
    members = Member.objects.filter(name__contains=keyword)
    return JsonResponse({"count": members.count()})
