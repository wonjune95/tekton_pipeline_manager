"""None 검사를 속이는 경우 — 모두 탐지되어야 한다.

종료처럼 보이는 호출(exit·quit·이름만 abort), 검사식을 다른 식으로 감싼 조건(&·|·not not·비교·호출 인자),
검사한 분기 안의 재대입, 검사보다 먼저 실행되는 사용, try 의 except·finally 본문, 다시 대입하기 전의 사용.
"""
import re

VERSION = re.compile(r"v(\d+)\.(\d+)")
DEFAULT = VERSION.search("v0.0")


def abort(code):
    print("rejected", code)


def audit(result):
    print("check", result)
    return False


def builtin_exit(text):
    m = VERSION.search(text)
    if m is None:
        exit(2)
    # 내장 exit() 는 site 모듈이 넣어 주는 대화형 도우미다 (python -S·임베디드 환경에는 없다) — import 로 확인되는 sys.exit 만 종료로 본다
    # ruleid: mois-5-01-null-dereference-py
    return m.group(1)


def builtin_quit(text):
    m = VERSION.search(text)
    if not m:
        quit()
    # 내장 quit() 도 같다
    # ruleid: mois-5-01-null-dereference-py
    return m.group(1)


def local_abort(text):
    m = VERSION.search(text)
    if m is None:
        abort(404)
    # 이 파일의 abort 는 기록만 하고 돌아온다 — 이름이 abort 일 뿐 중단하지 않는다
    # ruleid: mois-5-01-null-dereference-py
    return m.group(1)


def check_joined_with_bitand(text, strict):
    m = VERSION.search(text)
    if (m is None) & strict:
        return None
    # & 로 묶이면 strict 가 거짓일 때 None 이 그대로 내려온다
    # ruleid: mois-5-01-null-dereference-py
    return m.group(1)


def double_negation(text):
    m = VERSION.search(text)
    if not (not m):
        return None
    # not (not m) 은 뜻이 뒤집힌다: 값이 있으면 빠져나가고 None 일 때만 내려온다
    # ruleid: mois-5-01-null-dereference-py
    return m.group(1)


def check_compared_with_flag(text, strict):
    m = VERSION.search(text)
    if (m is None) == strict:
        return None
    # 검사 결과를 다른 값과 비교하면 strict 가 거짓일 때 None 이 내려온다
    # ruleid: mois-5-01-null-dereference-py
    return m.group(1)


def check_passed_to_call(text):
    m = VERSION.search(text)
    if audit(m is None):
        return None
    # 검사 결과를 다른 함수에 넘기면 그 함수가 무엇을 돌려주는지 알 수 없다
    # ruleid: mois-5-01-null-dereference-py
    return m.group(1)


def then_joined_with_bitor(text, strict):
    m = VERSION.search(text)
    if strict | (m is not None):
        # | 로 묶이면 strict 가 참일 때 None 이어도 들어온다
        # ruleid: mois-5-01-null-dereference-py
        return m.group(1)
    return None


def then_compared_with_false(text):
    m = VERSION.search(text)
    if (m is not None) is False:
        # is False 와 비교하면 뜻이 뒤집힌다: None 일 때만 들어온다
        # ruleid: mois-5-01-null-dereference-py
        return m.group(1)
    return None


def reassigned_inside_then(text, other):
    m = VERSION.search(text)
    if m:
        # 검사한 분기 안에서 다른 조회 결과로 바꿔 넣는다 — 새 값은 검사하지 않았다
        m = VERSION.search(other)
        # ruleid: mois-5-01-null-dereference-py
        return m.group(1)
    return None


def reassigned_inside_else(text, other):
    m = VERSION.search(text)
    if m is None:
        return None
    else:
        # else 쪽에서 다른 조회 결과로 바꿔 넣는다
        m = VERSION.search(other)
        # ruleid: mois-5-01-null-dereference-py
        return m.group(1)


def used_before_check_in_and(text, strict):
    m = VERSION.search(text)
    # and 는 왼쪽부터 실행한다 — m.group(1) 이 m 검사보다 먼저다
    # ruleid: mois-5-01-null-dereference-py
    return m.group(1) and m and strict


def used_in_except_body(text):
    m = VERSION.search(text)
    try:
        number = int(text)
    except ValueError:
        # except 본문의 예외는 이 try 가 잡아 주지 않는다
        # ruleid: mois-5-01-null-dereference-py
        number = int(m.group(1))
    return number


def used_in_else_and_finally(text, log):
    m = VERSION.search(text)
    try:
        number = int(text)
    except ValueError:
        number = 0
    else:
        # ruleid: mois-5-01-null-dereference-py
        log.debug("major=%s", m.group(1))
    finally:
        # ruleid: mois-5-01-null-dereference-py
        log.debug("minor=%s", m.group(2))
    return number


def used_in_finally_only(text, log):
    m = VERSION.search(text)
    try:
        number = int(text)
    except ValueError:
        number = 0
    finally:
        # ruleid: mois-5-01-null-dereference-py
        log.debug("minor=%s", m.group(2))
    return number


def used_in_else_only(text):
    m = VERSION.search(text)
    try:
        number = int(text)
    except ValueError:
        number = 0
    else:
        # ruleid: mois-5-01-null-dereference-py
        number += int(m.group(2))
    return number


def used_before_reassignment(text):
    m = VERSION.search(text)
    # 아래의 재대입보다 먼저 쓴다 — 이 시점의 m 은 None 일 수 있다
    # ruleid: mois-5-01-null-dereference-py
    major = m.group(1)
    m = DEFAULT
    return major, m.group(2)


def matched_again_after_default(text, other):
    m = VERSION.search(text)
    m = m or DEFAULT
    # 기본값을 채운 뒤에 다시 조회했다 — 마지막 값은 None 일 수 있다
    m = VERSION.search(other)
    # ruleid: mois-5-01-null-dereference-py
    return m.group(1)
