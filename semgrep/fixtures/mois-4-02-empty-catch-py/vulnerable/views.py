import json

from django.http import JsonResponse

from .models import AuditLog, Notice


def update_notice(request, notice_id):
    notice = Notice.objects.get(pk=notice_id)
    try:
        payload = json.loads(request.body)
        notice.title = payload["title"]
        notice.save()
    # ruleid: mois-4-02-empty-catch-py
    except (KeyError, ValueError):
        # 실패해도 아무 처리 없이 성공으로 응답
        pass
    try:
        AuditLog.objects.create(notice=notice, action="update")
    # ruleid: mois-4-02-empty-catch-py
    except Exception as e:
        ...
    finally:
        notice.refresh_from_db()
    return JsonResponse({"ok": True})


def import_notices(request):
    count = 0
    for line in request.FILES["file"]:
        try:
            Notice.objects.create(**json.loads(line))
        # ruleid: mois-4-02-empty-catch-py
        except ValueError:
            continue  # 잘못된 줄을 기록 없이 건너뜀
        count += 1
    try: count = int(count)
    # ruleid: mois-4-02-empty-catch-py
    except TypeError: pass
    return JsonResponse({"count": count})
