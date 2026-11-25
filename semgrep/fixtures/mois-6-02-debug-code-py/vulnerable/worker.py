"""만료 주문 정리 작업 (Django 설정을 직접 올려 쓰는 모듈)."""
import sys

import django

django.setup()

from portal.orders.models import Order  # noqa: E402


def purge_expired():
    expired = Order.objects.filter(status="expired")
    # 표준 출력으로 보내는 print 는 file= 이 있어도 디버그 출력이다
    # ruleid: mois-6-02-debug-code-py
    print("purging", expired.count(), file=sys.stdout)
    return expired.delete()


# 'import django' 형태로 가져온 웹 모듈에 남은 확인용 블록
# ruleid: mois-6-02-debug-code-py
if __name__ == "__main__":
    deleted = purge_expired()
    assert deleted is not None
