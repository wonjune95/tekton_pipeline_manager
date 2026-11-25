import contextlib
import logging
import os

from .services import SyncError, open_ticket, sync_members

logger = logging.getLogger(__name__)


def nightly_sync():
    try:
        sync_members()
    # ok: mois-4-03-improper-exception-handling-py 구체적인 예외만 잡고 처리한다
    except (ConnectionError, TimeoutError) as exc:
        logger.warning("sync postponed: %s", exc)
        return False
    return True


def sync_or_fail():
    try:
        sync_members()
    # ok: mois-4-03-improper-exception-handling-py 기록한 뒤 다른 예외로 바꿔 다시 던진다
    except Exception as exc:
        logger.exception("sync failed")
        raise SyncError("member sync failed") from exc


def sync_conditionally(strict):
    try:
        sync_members()
    # ok: mois-4-03-improper-exception-handling-py 조건에 따라 다시 던진다
    except Exception:
        logger.exception("sync failed")
        if strict: raise
        open_ticket("sync failed")


def sync_one_line():
    try:
        sync_members()
    # ok: mois-4-03-improper-exception-handling-py 한 줄로 다시 던진다
    except Exception: raise


def sync_by_mode(mode):
    try:
        sync_members()
    # ok: mois-4-03-improper-exception-handling-py `elif …: raise` 한 줄로 다시 던진다
    except Exception:
        if mode == "dry-run": logger.info("ignored in dry-run")
        elif mode == "strict": raise
        logger.exception("sync failed")


def sync_with_retry(retry):
    try:
        sync_members()
    # ok: mois-4-03-improper-exception-handling-py `else: raise` 한 줄로 다시 던진다
    except BaseException:
        if retry: sync_members()
        else: raise


def remove_marker(path):
    # ok: mois-4-03-improper-exception-handling-py 없어도 되는 파일만 조용히 넘긴다 (특정 예외)
    with contextlib.suppress(FileNotFoundError):
        os.remove(path)
