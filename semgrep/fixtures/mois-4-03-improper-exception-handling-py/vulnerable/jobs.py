import logging

from .services import open_ticket, sync_members

logger = logging.getLogger(__name__)


def nightly_sync():
    try:
        sync_members()
    # ruleid: mois-4-03-improper-exception-handling-py
    except Exception:
        logger.error("sync failed")


def sync_with_ticket():
    try:
        sync_members()
    # ruleid: mois-4-03-improper-exception-handling-py
    except (OSError, Exception) as exc:
        # 주석이나 문자열 안의 raise 는 다시 던진 것이 아니다 (do not raise here)
        logger.error("could not raise ticket: %s", exc)
        return None


def sync_with_fallback():
    try:
        sync_members()
    # ruleid: mois-4-03-improper-exception-handling-py
    except BaseException as exc:
        try:
            open_ticket(str(exc))
        except OSError:
            logger.warning("ticket system down")
    return True


def sync_with_todo(strict):
    try:
        sync_members()
    # ruleid: mois-4-03-improper-exception-handling-py
    except Exception:
        # 조건문 줄 끝의 주석에 적은 raise 는 다시 던진 것이 아니다
        if strict: logger.error("strict sync failed")  # TODO: raise
        open_ticket("sync failed")


class Batch:
    def run(self):
        for step in self.steps:
            try:
                step()
            # ruleid: mois-4-03-improper-exception-handling-py
            except Exception as exc:
                self.errors.append(exc)
                continue
