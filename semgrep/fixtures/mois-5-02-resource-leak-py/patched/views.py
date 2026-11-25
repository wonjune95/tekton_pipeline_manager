import sqlite3
from contextlib import closing

from django.conf import settings
from django.http import FileResponse, HttpResponse, JsonResponse


def read_notice(request):
    with open(settings.NOTICE_FILE, encoding="utf-8") as f:
        return HttpResponse(f.read())


def write_log(request):
    log = open(settings.ACCESS_LOG, "a", encoding="utf-8")
    try:
        log.write(request.META.get("REMOTE_ADDR", "-") + "\n")
    finally:
        log.close()
    return HttpResponse("ok")


def stats(request):
    conn = sqlite3.connect(settings.STATS_DB)
    with closing(conn):
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM visit")
        return JsonResponse({"count": cur.fetchone()[0]})


def download_notice(request):
    # 응답 객체가 파일을 닫는다
    f = open(settings.NOTICE_FILE, "rb")
    return FileResponse(f)


def read_banner(request):
    try:
        banner = open(settings.BANNER_FILE, encoding="utf-8")
    except FileNotFoundError:
        return HttpResponse("")
    with banner:
        return HttpResponse(banner.read(), content_type="text/plain")
