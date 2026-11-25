#!/usr/bin/env python3
"""가지별 변이 시험 — "규칙의 가지마다 fixture 가 있는가"를 확인한다.

    docker run --rm --network none -v "$PWD":/src:ro -w /src semgrep/semgrep:1.180.0 python3 scripts/mutate.py [<rule-id> ...]

인자가 없으면 모든 규칙을 본다. 규칙의 아래 조각을 **하나씩 지운 변이 규칙**을 만들어 fixture 결과가 달라지는지 본다.

  - pattern-either 가지, sink, sanitizer, 제외(pattern-not · pattern-not-inside · pattern-not-regex)
  - 정규식(metavariable-regex · pattern-regex · pattern-not-regex) 안의 모든 대안 묶음 (a|b|c) — 겹쳐진 묶음과 부정 전방 탐색 목록 포함
  - 규칙 고유 source

결과가 그대로인 변이("살아남은 변이")는 그 조각이 죽었거나, 다른 조각과 중복이거나, 예제가 없다는 뜻이다.
모든 규칙이 `기준 일치, 살아남은 변이 0개` 여야 한다 (아니면 종료코드 1).

변이하지 않는 것 (여러 규칙이 같은 블록을 복사해 쓰므로 한 곳에서만 본다):
  - 공통 source 블록: Java 는 os-command-injection.yaml, Python 은 docs/python-source-block.yaml 의 항목과 같은 것
  - propagator
  - Python 공통 sanitizer (공통 1~3, docs/python-source-block.yaml 의 항목과 같은 것) — SHARED_OWNER 규칙에서만 변이한다
  - metavariable-comparison 의 경계값, 문자 클래스 안의 글자
"""
import copy, json, os, re, subprocess, sys, tempfile
from pathlib import Path

from ruamel.yaml import YAML

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / 'scripts'))
import expect  # noqa: E402

SHARED_OWNER = 'mois-1-05-os-command-injection-py'
RID = ''
yaml = YAML(typ='safe')
yaml.default_flow_style = False
yaml.width = 1 << 20
yaml.allow_unicode = True


def _shared_sources():
    out = []
    java = yaml.load(REPO / 'rules/mois/01-input-validation/os-command-injection.yaml')['rules'][0]['pattern-sources']
    py = yaml.load(REPO / 'docs/python-source-block.yaml')['pattern-sources']
    return list(java) + list(py)


SHARED_SOURCES = _shared_sources()
# Python 공통 sanitizer 는 문서의 블록과 "같은 항목"만 공통으로 본다 (이름이 우연히 같은 규칙 고유 sanitizer 는 변이한다)
SHARED_SANITIZERS = list(yaml.load(REPO / 'docs/python-source-block.yaml')['pattern-sanitizers'])

def walk(node, path=()):
    """(path, description) 변이 지점"""
    if isinstance(node, dict):
        for k, v in node.items():
            if k in ('pattern-propagators', 'metadata'):
                continue
            if k == 'pattern-sources' and isinstance(v, list):
                # 공통 source 블록의 항목은 건너뛰고, 규칙 고유 source 만 변이한다
                own = [i for i, it in enumerate(v) if it not in SHARED_SOURCES]
                for i in own:
                    if len(v) > 1:
                        yield ('del', path + (k, i)), f'{k}[{i}] 삭제: {short(v[i])}'
                for i in own:
                    yield from walk(v[i], path + (k, i))
                continue
            if k == 'pattern-sanitizers' and isinstance(v, list) and RID != SHARED_OWNER:
                keep = [i for i, it in enumerate(v) if it not in SHARED_SANITIZERS]
                for i in keep:
                    if len(v) > 1:
                        yield ('del', path + (k, i)), f'{k}[{i}] 삭제: {short(v[i])}'
                for i in keep:
                    yield from walk(v[i], path + (k, i))
                continue
            if k in ('pattern-either', 'pattern-sinks', 'pattern-sanitizers') and isinstance(v, list) and (len(v) > 1 or k != 'pattern-either'):
                for i in range(len(v)):
                    if len(v) > 1:
                        yield ('del', path + (k, i)), f'{k}[{i}] 삭제: {short(v[i])}'
            if k == 'patterns' and isinstance(v, list):
                for i, it in enumerate(v):
                    if isinstance(it, dict) and (set(it) & {'pattern-not', 'pattern-not-inside', 'pattern-not-regex'}):
                        yield ('del', path + (k, i)), f'제외[{i}] 삭제: {short(it)}'
            if k == 'metavariable-regex' and isinstance(v, dict):
                rx = v.get('regex', '')
                # 확장: 맨 끝 그룹뿐 아니라 모든 그룹(중첩 포함)의 최상위 대안을 하나씩 지운다
                for s, e, cuts in groups(rx):
                    bounds = [s] + cuts + [e]
                    alts = [(bounds[i] + (1 if i else 0), bounds[i + 1]) for i in range(len(bounds) - 1)]
                    for n, (x, y) in enumerate(alts):
                        new = rx[:x - 1] + rx[y:] if n else rx[:x] + rx[y + 1:]
                        yield ('set', path + (k, 'regex'), new), f'정규식 대안 삭제 {v.get("metavariable")}: {rx[x:y]}   => {new}'
            if k in ('pattern-regex', 'pattern-not-regex') and isinstance(v, str):
                for s, e, cuts in groups(v):
                    bounds = [s] + cuts + [e]
                    alts = [(bounds[i] + (1 if i else 0), bounds[i + 1]) for i in range(len(bounds) - 1)]
                    for n, (x, y) in enumerate(alts):
                        new = v[:x - 1] + v[y:] if n else v[:x] + v[y + 1:]
                        yield ('set', path + (k,), new), f'{k} 대안 삭제: {v[x:y]}   (그룹 {v[s:e][:50]})'
            yield from walk(v, path + (k,))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk(v, path + (i,))

def groups(rx):
    """(내용 시작, 내용 끝, 최상위 | 위치들) — 대안이 2개 이상인 그룹만. 문자 클래스·이스케이프는 건너뛴다."""
    out, stack, i, incls = [], [], 0, False
    while i < len(rx):
        c = rx[i]
        if c == '\\':
            i += 2; continue
        if incls:
            incls = c != ']'
        elif c == '[':
            incls = True
            i += 2 if rx.startswith('^', i + 1) else 1      # 맨 앞의 ] 는 글자다: []x], [^]x]
            if rx.startswith(']', i): i += 1
            continue
        elif c == '(':
            j = i + 1
            if rx.startswith('?', j):
                j += 2 if rx[j + 1] in ':!=' else (3 if rx[j + 1] == '<' else 0)
                m = re.match(r'\(\?[a-zA-Z]+\)', rx[i:])   # (?i) (?m) (?im) 플래그
                if m:
                    i += m.end(); continue
            m = re.match(r'\(\?[a-zA-Z]+:', rx[i:])       # (?i:...) 묶음
            if m: j = i + m.end()
            stack.append([j, []])
        elif c == ')':
            if not stack:      # 짝이 안 맞는 정규식은 건드리지 않는다
                return []
            s, cuts = stack.pop()
            if cuts:
                out.append((s, i, cuts))
        elif c == '|' and stack:
            stack[-1][1].append(i)
        i += 1
    return sorted(out)

def short(x):
    s = json.dumps(x, ensure_ascii=False)
    return s[:150]

def apply(rule, mut):
    r = copy.deepcopy(rule)
    kind, path = mut[0], mut[1]
    cur = r
    for p in path[:-1]:
        cur = cur[p]
    if kind == 'del':
        del cur[path[-1]]
    else:
        cur[path[-1]] = mut[2]
    return r

def scan(cfg, d):
    o = tempfile.mktemp(suffix='.json')
    subprocess.run(['semgrep', 'scan', '--config', cfg, '--metrics=off', '--disable-version-check', '--json', '-o', o, '-q', '.'],
                   cwd=REPO / d, capture_output=True, text=True)
    data = json.load(open(o, encoding='utf-8'))
    os.unlink(o)
    for e in data['errors']:
        print('   semgrep error:', e.get('message', '')[:300])
    res = {}
    for r in data['results']:
        res.setdefault(r['check_id'].rsplit('.', 1)[-1], set()).add((r['path'].lstrip('./'), r['start']['line']))
    return res


def all_rules():
    found = {}
    for f in sorted((REPO / 'rules').rglob('*.yaml')):
        for r in yaml.load(f)['rules']:
            found[r['id']] = r
    return found


def main():
    global RID
    rules = all_rules()
    ids = sys.argv[1:] or sorted(rules)
    failed = 0
    for rid in ids:
        RID = rid
        rule = rules[rid]
        muts = list(walk(rule))
        v, p = {}, {}
        # 변이 규칙이 많으면 한 번에 돌릴 때 semgrep 이 "Too many matches" 를 내므로 나눠 돌린다
        for lo in range(0, max(len(muts), 1), 40):
            variants = []
            for i in range(lo, min(lo + 40, len(muts))):
                r = apply(rule, muts[i][0])
                r['id'] = f'm{i}'
                variants.append(r)
            base = copy.deepcopy(rule)
            base['id'] = 'base'
            variants.append(base)
            with tempfile.NamedTemporaryFile('w', suffix='.yaml', delete=False, encoding='utf-8') as t:
                yaml.dump({'rules': variants}, t)
            v.update(scan(t.name, f'fixtures/{rid}/vulnerable'))
            p.update(scan(t.name, f'fixtures/{rid}/patched'))
            os.unlink(t.name)
        exp = expect.expected(REPO / 'fixtures' / rid / 'vulnerable', rid)
        okb = v.get('base', set()) == exp and not p.get('base')
        surv = [(i, d) for i, (_, d) in enumerate(muts) if v.get(f'm{i}', set()) == exp and not p.get(f'm{i}')]
        print(f'{rid}: 변이 {len(muts)}개, 기준 {"일치" if okb else "불일치!"}, 살아남은 변이 {len(surv)}개', flush=True)
        for i, d in surv:
            print(f'   [m{i}] {d}')
        failed += (not okb) + len(surv)
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
