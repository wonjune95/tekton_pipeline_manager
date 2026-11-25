import json
import logging

from django.db import DatabaseError
from django.http import JsonResponse

from .models import AuditLog, Notice

logger = logging.getLogger(__name__)


def update_notice(request, notice_id):
    notice = Notice.objects.get(pk=notice_id)
    try:
        payload = json.loads(request.body)
        notice.title = payload["title"]
        notice.save()
    except (KeyError, ValueError):
        logger.warning("invalid notice update payload: notice=%s", notice_id)
        return JsonResponse({"ok": False, "error": "E400"}, status=400)
    try:
        AuditLog.objects.create(notice=notice, action="update")
    except DatabaseError:
        logger.exception("audit log write failed")
        raise
    return JsonResponse({"ok": True})


def import_notices(request):
    count = 0
    skipped = 0
    for line in request.FILES["file"]:
        try:
            Notice.objects.create(**json.loads(line))
        except ValueError:
            # 건너뛴 줄은 기록하고 결과에 포함
            logger.warning("skip invalid notice line")
            skipped += 1
            continue
        count += 1
    return JsonResponse({"count": count, "skipped": skipped})
