import logging

from django.http import JsonResponse

logger = logging.getLogger(__name__)
audit_log = logging.getLogger("audit")


def render_card(request):
    layout = request.POST.get("layout", "{title}")
    # format_map 도 형식 문자열을 해석한다
    # ruleid: mois-1-17-format-string-py
    text = layout.format_map({"title": "공지", "owner": request.user})
    return JsonResponse({"text": text})


def record(request):
    note = request.POST.get("note", "")
    # 수준을 인자로 받는 log(level, 형식, 인자…)
    # ruleid: mois-1-17-format-string-py
    audit_log.log(logging.WARNING, "note=" + note + " by %s", request.user.pk)
    # ruleid: mois-1-17-format-string-py
    logger.warning(note + " (user=%s)", request.user.pk)
    return JsonResponse({"ok": True})


def int_result_discarded(request):
    width = request.GET.get("width", "10")
    # 숫자로 바꾼 결과를 쓰지 않음
    int(width)
    # ruleid: mois-1-17-format-string-py
    return JsonResponse({"label": ("%" + width + "s|") % "x"})


def record_levels(request):
    note = request.POST.get("note", "")
    # logging 의 나머지 수준별 메서드 — 인자가 있으면 메시지가 % 형식으로 해석된다
    # ruleid: mois-1-17-format-string-py
    logger.debug("debug " + note + " (user=%s)", request.user.pk)
    # ruleid: mois-1-17-format-string-py
    logger.warn(note + " (user=%s)", request.user.pk)
    # ruleid: mois-1-17-format-string-py
    logger.error("failed: " + note + " (user=%s)", request.user.pk)
    try:
        request.user.profile.refresh_from_db()
    except Exception:
        # ruleid: mois-1-17-format-string-py
        logger.exception(note + " (user=%s)", request.user.pk)
    # ruleid: mois-1-17-format-string-py
    audit_log.critical(note + " (user=%s)", request.user.pk)
    # ruleid: mois-1-17-format-string-py
    audit_log.fatal(note + " (user=%s)", request.user.pk)
    return JsonResponse({"ok": True})
