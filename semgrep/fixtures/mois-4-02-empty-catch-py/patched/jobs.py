import contextlib
import logging
import os

from .services import parse_row

logger = logging.getLogger(__name__)


def cleanup(paths):
    for path in paths:
        # ok: mois-4-02-empty-catch-py 없어도 되는 파일이라는 뜻을 드러낸 suppress (특정 예외)
        with contextlib.suppress(FileNotFoundError):
            os.remove(path)


def import_rows(rows):
    result = []
    for row in rows:
        try:
            result.append(parse_row(row))
        # ok: mois-4-02-empty-catch-py 기록하고 다시 던진다
        except ValueError:
            logger.exception("invalid row")
            raise
    return result


def import_rows_lenient(rows):
    result, failed = [], 0
    for row in rows:
        try:
            result.append(parse_row(row))
        # ok: mois-4-02-empty-catch-py pass 뒤에 실제 처리가 이어진다
        except ValueError:
            pass
            failed += 1
    return result, failed


def read_optional(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    # ok: mois-4-02-empty-catch-py 기본값을 돌려준다
    except FileNotFoundError:
        return ""


def except_in_text():
    # ok: mois-4-02-empty-catch-py except 라는 낱말로 시작하지 않는 줄
    exception_note = "handled"
    return exception_note
