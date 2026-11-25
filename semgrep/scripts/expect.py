#!/usr/bin/env python3
"""fixture 의 기대 탐지 위치와 semgrep 결과를 정확히 비교한다.

  expect.py <semgrep.json> <rule-id> <fixture 디렉터리(vulnerable 또는 patched)>

기대 위치는 fixture 파일의 주석으로 적는다. 주석 다음에 오는 첫 코드 줄이 탐지되어야 한다.

    // ruleid: mois-1-01-sql-injection-jdbc        (Java)
    # ruleid: mois-1-01-sql-injection-py           (Python)
    <!-- ruleid: mois-1-01-sql-injection-mybatis --> (XML)

주석을 넣을 수 없는 파일(의존성 목록 등)은 <fixture 디렉터리>/expected.txt 에 `상대경로:줄` 을 한 줄씩 적는다.
표시가 없는 줄이 탐지되거나 표시한 줄이 탐지되지 않으면 실패한다 (patched 는 표시가 없으므로 0건이어야 한다).
`ok: <rule-id>` 주석은 "여기는 탐지되면 안 된다"는 설명용이며 검사에는 쓰지 않는다.
"""
import json
import re
import sys
from pathlib import Path

MARK = re.compile(r'ruleid:\s*([a-z0-9-]+)')
ANNOT = re.compile(r"^\s*(//|#|<!--|/\*|\*|\{/\*)\s*(ruleid|ok):")


def expected(root, rule_id):
    exp = set()
    side = root / 'expected.txt'
    if side.exists():
        for line in side.read_text(encoding='utf-8').splitlines():
            line = line.split('#', 1)[0].strip()
            if line:
                path, _, no = line.rpartition(':')
                exp.add((path, int(no)))
    for f in sorted(p for p in root.rglob('*') if p.is_file() and p.name != 'expected.txt'):
        try:
            lines = f.read_text(encoding='utf-8').splitlines()
        except UnicodeDecodeError:
            continue
        for i, line in enumerate(lines):
            if not ANNOT.match(line):
                continue
            if rule_id not in MARK.findall(line):
                continue
            j = i + 1
            while j < len(lines) and (not lines[j].strip() or ANNOT.match(lines[j])):
                j += 1
            if j < len(lines):
                exp.add((str(f.relative_to(root)), j + 1))
    return exp


def main():
    out, rule_id, root = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    data = json.load(open(out, encoding='utf-8'))
    for e in data['errors']:
        print('       semgrep error:', e.get('message', '')[:200])
    if data['errors']:
        return 1
    actual = {(r['path'].lstrip('./'), r['start']['line']) for r in data['results']
              if r['check_id'].rsplit('.', 1)[-1] == rule_id}
    exp = expected(root, rule_id)
    missing, extra = sorted(exp - actual), sorted(actual - exp)
    for p, n in missing:
        print(f'       표시했지만 탐지되지 않음: {p}:{n}')
    for p, n in extra:
        print(f'       표시 없이 탐지됨: {p}:{n}')
    print(len(actual))
    return 1 if missing or extra else 0


if __name__ == '__main__':
    sys.exit(main())
