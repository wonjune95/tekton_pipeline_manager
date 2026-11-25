import logging

from .services import sync_members

logger = logging.getLogger(__name__)


# 이 파일은 일부러 마지막 줄 끝에 줄바꿈을 두지 않는다 (except 본문이 파일 끝에서 끝나는 경우)
def last_job():
    try:
        sync_members()
    # ruleid: mois-4-03-improper-exception-handling-py
    except Exception:
        logger.error("sync failed")