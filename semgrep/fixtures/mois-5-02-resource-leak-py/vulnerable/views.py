import sqlite3

from django.conf import settings
from django.http import HttpResponse, JsonResponse


def read_notice(request):
    # 닫지 않음: 예외가 없어도 파일 핸들이 남음
    # ruleid: mois-5-02-resource-leak-py
    f = open(settings.NOTICE_FILE, encoding="utf-8")
    return HttpResponse(f.read())


def write_log(request):
    # ruleid: mois-5-02-resource-leak-py
    log = open(settings.ACCESS_LOG, "a", encoding="utf-8")
    log.write(request.META.get("REMOTE_ADDR", "-") + "\n")  # 여기서 예외가 나면 닫히지 않음
    log.close()
    return HttpResponse("ok")


def stats(request):
    # ruleid: mois-5-02-resource-leak-py
    conn = sqlite3.connect(settings.STATS_DB)  # 연결을 닫지 않음
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM visit")
    return JsonResponse({"count": cur.fetchone()[0]})
