#!/usr/bin/env python3
"""Semgrep 보안점검 보조 스크립트. semgrep 이미지의 python3 로 실행한다
(표준 라이브러리 + semgrep 에 포함된 ruamel.yaml, 설치 작업 없음).

  report.py check-rules <규칙 디렉터리>   규칙 메타데이터 검사, 규칙 목록을 JSON 으로 출력
  report.py preflight                     Task preflight step: 입력값·규칙·대상 검사 → $OUT_DIR/context.json
  report.py report                        Task report step: semgrep.json → 로그 보고서, results, 게이트 판정

preflight/report 는 Task 파라미터를 환경변수로 받는다 (semgrep-security-scan Task 의 stepTemplate 참고).
"""
import fnmatch
import json
import os
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

REQUIRED = {
    'mois': ('mois-guide', 'mois-category', 'mois-item-no', 'mois-item', 'cwe', 'gate'),
    'cve': ('cve', 'cvss', 'severity-label', 'fixed-version', 'references', 'gate'),
}
SEVERITIES = ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW')
THRESHOLDS = ('MAX_MOIS_BLOCK', 'MAX_MOIS_WARN', 'MAX_CVE_CRITICAL', 'MAX_CVE_HIGH', 'MAX_CVE_MEDIUM')
GATE_ROWS = (('행안부 block', 'MAX_MOIS_BLOCK'), ('행안부 warn', 'MAX_MOIS_WARN'),
             ('CVE CRITICAL', 'MAX_CVE_CRITICAL'), ('CVE HIGH', 'MAX_CVE_HIGH'), ('CVE MEDIUM', 'MAX_CVE_MEDIUM'))
# CVE 규칙(r2c-internal-project-depends-on)이 읽는 의존성 파일.
# maven 은 1.180.0 실측: pom.xml 은 읽지 않고 maven_dep_tree.txt(mvn dependency:tree 출력)·gradle.lockfile 만 읽는다.
# npm·pypi·gomod 는 작업 지시서 4.5 기준이며, 그 생태계 첫 CVE 규칙의 fixture 로 확인한다.
LOCKFILES = {
    'maven': ('maven_dep_tree.txt', 'gradle.lockfile'),
    'npm': ('package-lock.json', 'yarn.lock', 'pnpm-lock.yaml'),
    'pypi': ('*requirement*.txt', 'poetry.lock', 'Pipfile.lock', 'uv.lock'),
    'gomod': ('go.mod',),
}
ECOSYSTEM = {'maven': 'Maven', 'npm': 'npm', 'pypi': 'Python', 'gomod': 'Go'}
LOCKFILE_HINT = {'maven': 'pom.xml 만으로는 인식되지 않음 — 빌드에서 mvn dependency:tree -DoutputFile=maven_dep_tree.txt 생성'}
LINE, RULE = '=' * 64, '-' * 64


def width(s):
    return sum(2 if unicodedata.east_asian_width(c) in 'WF' else 1 for c in str(s))


def pad(s, n, right=False):
    """고정폭 로그 정렬. 한글은 2칸으로 센다."""
    fill = ' ' * max(n - width(s), 0)
    return f'{fill}{s}' if right else f'{s}{fill}'


def load_rules(rules_dir):
    """규칙 파일을 읽어 (규칙 목록, 오류 목록)을 돌려준다. 규칙 = {id, file, type, namespaces}"""
    from ruamel.yaml import YAML
    yaml = YAML(typ='safe')
    rules, errors, seen = [], [], {}
    files = sorted(p for p in Path(rules_dir).rglob('*') if p.is_file() and p.suffix in ('.yaml', '.yml'))
    for f in files:
        try:
            doc = yaml.load(f) or {}
        except Exception as e:
            errors.append(f'{f}: YAML 파싱 실패 — {e}')
            continue
        for r in doc.get('rules') or []:
            rid = str(r.get('id', ''))
            where = f'{f}: {rid or "(id 없음)"}'
            meta = r.get('metadata') or {}
            kind = meta.get('rule-type')
            if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', rid):
                errors.append(f'{where}: id 는 소문자·숫자·하이픈만 쓴다')
                continue
            if rid in seen:
                errors.append(f'{where}: id 중복 ({seen[rid]})')
                continue
            seen[rid] = f
            if kind not in REQUIRED:
                errors.append(f'{where}: metadata.rule-type 은 mois 또는 cve')
                continue
            missing = [k for k in REQUIRED[kind] if meta.get(k) in (None, '', [])]
            if missing:
                errors.append(f'{where}: 필수 메타데이터 누락 {", ".join(missing)}')
            if meta.get('gate') not in ('block', 'warn'):
                errors.append(f'{where}: gate 는 block 또는 warn')
            namespaces = []
            if kind == 'cve':
                if not re.fullmatch(r'CVE-\d{4}-\d{4,}', str(meta.get('cve', ''))):
                    errors.append(f'{where}: cve 는 CVE-YYYY-NNNN 형식')
                if meta.get('severity-label') not in SEVERITIES:
                    errors.append(f'{where}: severity-label 은 {"/".join(SEVERITIES)}')
                dep = r.get('r2c-internal-project-depends-on') or {}
                entries = dep.get('depends-on-either') or ([dep] if dep else [])
                if not entries:
                    errors.append(f'{where}: r2c-internal-project-depends-on 없음')
                namespaces = sorted({str(e.get('namespace', '')).lower() for e in entries})
                unknown = [n for n in namespaces if n not in LOCKFILES]
                if unknown:
                    errors.append(f'{where}: 알 수 없는 namespace {unknown} (maven/npm/pypi/gomod)')
            rules.append({'id': rid, 'file': str(f), 'type': kind, 'namespaces': namespaces})
    if not rules and not errors:
        errors.append(f'{rules_dir}: 규칙 0개')
    return rules, errors


def check_rules(rules_dir):
    rules, errors = load_rules(rules_dir)
    for m in errors:
        print(f'  - {m}', file=sys.stderr)
    if errors:
        return 1
    print(json.dumps({'count': len(rules), 'rules': rules}, ensure_ascii=False))
    return 0


def git(cwd, *args):
    r = subprocess.run(['git', '-C', str(cwd), *args], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def target_files(target):
    """semgrep 과 같은 기준의 대상 파일 목록: git 저장소면 추적 파일 + 무시되지 않은 새 파일."""
    listed = git(target, 'ls-files', '--cached', '--others', '--exclude-standard')
    if listed is not None:
        return listed.splitlines()
    return [str(p.relative_to(target)) for p in Path(target).rglob('*')
            if p.is_file() and '.git' not in p.parts and 'node_modules' not in p.parts]


def preflight():
    env = os.environ

    def fail(msg):
        print(f'[preflight] 실패: {msg}', file=sys.stderr)
        return 1

    rules_path = env.get('RULES_PATH', '')
    if re.match(r'(p/|r/|s/|auto|http)', rules_path):
        return fail(f'RULES_PATH={rules_path} — 원격 설정(p/ r/ s/ auto http)은 폐쇄망에서 쓸 수 없다. '
                    'rules 워크스페이스 기준 상대경로를 지정한다')
    if rules_path.startswith('/'):
        return fail(f'RULES_PATH={rules_path} — rules 워크스페이스 기준 상대경로여야 한다')
    for k in THRESHOLDS:
        if not re.fullmatch(r'-1|\d+', env.get(k, '')):
            return fail(f'{k}={env.get(k, "")!r} — -1(무제한) 이상의 정수여야 한다')
    if not re.fullmatch(r'[1-9]\d*', env.get('TIMEOUT_SEC', '')):
        return fail(f'TIMEOUT_SEC={env.get("TIMEOUT_SEC", "")!r} — 1 이상의 정수여야 한다')
    if env.get('CVE_REACHABLE_ONLY') not in ('true', 'false'):
        return fail(f'CVE_REACHABLE_ONLY={env.get("CVE_REACHABLE_ONLY", "")!r} — true 또는 false')

    rules_root = Path(env['RULES_ROOT'])
    rules_dir = rules_root / rules_path
    target = Path(env['SRC_ROOT']) / env.get('TARGET_PATH', '.')
    if not rules_dir.is_dir():
        return fail(f'규칙 디렉터리 없음: {rules_dir}')
    if not target.is_dir():
        return fail(f'점검 대상 디렉터리 없음: {target}')
    rules, errors = load_rules(rules_dir)
    for m in errors:
        print(f'  - {m}', file=sys.stderr)
    if errors:
        return fail('규칙 검사 실패 (위 목록)')

    # 규칙을 이미지에 넣은 경우 git 이 없으므로 이미지 빌드 때 쓴 VERSION 파일("<태그> <커밋>")을 읽는다
    version_file = rules_root / 'VERSION'
    if version_file.is_file():
        tag, _, commit = version_file.read_text(encoding='utf-8').strip().partition(' ')
        tag, commit = tag or 'untagged', commit or 'unknown'
    else:
        tag = git(rules_root, 'describe', '--tags', '--exact-match', 'HEAD') or 'untagged'
        commit = git(rules_root, 'rev-parse', '--short', 'HEAD') or 'unknown'
    url = git(target, 'remote', 'get-url', 'origin')
    repo = re.sub(r'\.git$', '', url.rstrip('/').rsplit('/', 1)[-1]) if url else target.resolve().name
    head = git(target, 'rev-parse', '--short', 'HEAD') or 'unknown'
    ref = env.get('BASELINE_REF', '')
    scope = '전체'
    if ref:
        base = git(target, 'rev-parse', '--verify', '--quiet', ref + '^{commit}')
        if not base:
            return fail(f"기준 커밋 '{ref}' 을 찾을 수 없다 — git-clone 의 depth 를 늘리거나(0=전체) "
                        '기준 브랜치를 함께 fetch 해야 한다')
        dirty = git(target, 'status', '--porcelain', '--untracked-files=no')
        if dirty:
            return fail('추적 파일이 바뀐 상태라 신규 코드 점검을 할 수 없다 '
                        f'(semgrep baseline 은 깨끗한 작업트리 필요):\n{dirty}')
        scope = f'신규(기준 {ref}@{base[:7]})'

    namespaces = sorted({n for r in rules for n in r['namespaces']})
    files = target_files(target) if namespaces else []
    lockfiles = {ns: sorted(f for f in files if any(fnmatch.fnmatch(Path(f).name, p) for p in LOCKFILES[ns]))
                 for ns in namespaces}

    out = Path(env['OUT_DIR'])
    out.mkdir(parents=True, exist_ok=True)
    ctx = {'tag': tag, 'commit': commit, 'ruleset': f'{tag}@{commit}', 'rules': rules,
           'target': {'repo': repo, 'commit': head}, 'scope': scope, 'lockfiles': lockfiles}
    (out / 'context.json').write_text(json.dumps(ctx, ensure_ascii=False, indent=1))

    n_mois = sum(r['type'] == 'mois' for r in rules)
    print(f'[preflight] 규칙셋 security-rules {tag} ({commit}) — 규칙 {len(rules)}개 '
          f'(행안부 {n_mois}, CVE {len(rules) - n_mois})')
    print(f'[preflight] 대상 {repo}@{head}   점검 범위: {scope}')
    for ns, found in lockfiles.items():
        print(f'[preflight] 의존성 파일 {ECOSYSTEM[ns]}: {", ".join(found) or "없음"}')
    print('[preflight] 기준치 ' + '  '.join(f'{k}={env[k]}' for k in THRESHOLDS)
          + f'  CVE_REACHABLE_ONLY={env["CVE_REACHABLE_ONLY"]}')
    return 0


def report():
    env = os.environ
    out = Path(env['OUT_DIR'])
    try:
        ctx = json.loads((out / 'context.json').read_text())
        res = json.loads((out / 'semgrep.json').read_text())
        results, errors = res['results'], res['errors']
    except (OSError, ValueError, KeyError) as e:
        print(f'[report] 실패: 결과 파일을 읽지 못함 — {e}', file=sys.stderr)
        return 1
    lim = {k: int(env[k]) for k in THRESHOLDS}
    reach_only = env.get('CVE_REACHABLE_ONLY') == 'true'

    mois, cve = [], []
    for r in results:
        m = r['extra'].get('metadata') or {}
        loc = {'path': r['path'], 'line': r['start']['line']}
        if m.get('rule-type') == 'cve':
            sca = r['extra'].get('sca_info') or {}
            dep = (sca.get('dependency_match') or {}).get('found_dependency') or {}
            cve.append({**loc, 'cve': m.get('cve', '?'), 'sev': m.get('severity-label', '?'),
                        'gate': m.get('gate', 'block'), 'package': str(dep.get('package', '?')).split(':')[-1],
                        'version': dep.get('version', '?'), 'fixed': m.get('fixed-version', '?'),
                        'reachable': bool(sca.get('reachable'))})
        else:
            mois.append({**loc, 'category': m.get('mois-category', '?'), 'item': m.get('mois-item', '?'),
                         'cwe': m.get('cwe', '?'), 'gate': m.get('gate', 'block')})

    count = {'MAX_MOIS_BLOCK': sum(f['gate'] == 'block' for f in mois),
             'MAX_MOIS_WARN': sum(f['gate'] == 'warn' for f in mois)}
    for s in ('CRITICAL', 'HIGH', 'MEDIUM'):
        # CVE 는 등급별 기준치로 판정. gate: warn 규칙과 (reachable 만 집계 시) 미도달은 보고만 한다
        count[f'MAX_CVE_{s}'] = sum(f['sev'] == s and f['gate'] == 'block' and (f['reachable'] or not reach_only)
                                    for f in cve)
    over = [(label, count[k]) for label, k in GATE_ROWS if lim[k] != -1 and count[k] > lim[k]]
    if errors:
        over.append(('Semgrep 오류', len(errors)))
    gate = 'FAIL' if over else 'PASS'

    rules = ctx['rules']
    n_mois_rules = sum(r['type'] == 'mois' for r in rules)
    scanned = len((res.get('paths') or {}).get('scanned') or [])
    reach = sum(f['reachable'] for f in cve)
    p = print
    p(LINE)
    p(' Semgrep 보안점검 결과')
    p(f' 규칙셋 : security-rules {ctx["tag"]} ({ctx["commit"]})   Semgrep {res.get("version", "?")}   규칙 {len(rules)}개')
    p(f' 대상   : {ctx["target"]["repo"]}@{ctx["target"]["commit"]}   스캔 파일 {scanned:,}개')
    p(f' 점검 범위: {ctx["scope"]}')
    p(LINE)
    p()
    p(f'[1] 행안부 보안약점   총 {len(mois)}건 (block {count["MAX_MOIS_BLOCK"]} / warn {count["MAX_MOIS_WARN"]})')
    p(RULE)
    if mois:
        groups = {}
        for f in mois:
            groups.setdefault((f['gate'] != 'block', f['category'], f['item'], f['cwe'], f['gate']), []).append(f)
        p(' ' + pad('분류', 26) + pad('항목', 20) + pad('CWE', 10) + pad('건수', 4, True) + '  게이트')
        for (_, cat, item, cwe, g), fs in sorted(groups.items()):
            p(' ' + pad(cat, 26) + pad(item, 20) + pad(cwe, 10) + pad(len(fs), 4, True) + '  ' + g)
        p()
        for f in sorted(mois, key=lambda f: (f['gate'] != 'block', f['path'], f['line'])):
            p(f'  - [{f["gate"]:<5}] {f["item"]}  {f["path"]}:{f["line"]}')
    else:
        p(f'  탐지 없음 (행안부 규칙 {n_mois_rules}개 적용)')
    p()
    p(f'[2] CVE   총 {len(cve)}건 (reachable {reach} / unreachable {len(cve) - reach})')
    p(RULE)
    if cve:
        p(' ' + pad('CVE', 17) + pad('등급', 10) + pad('패키지', 18) + pad('현재', 10) + pad('조치버전', 26) + '도달')
        order = {s: i for i, s in enumerate(SEVERITIES)}
        for f in sorted(cve, key=lambda f: (order.get(f['sev'], 9), f['cve'], f['path'], f['line'])):
            p(' ' + pad(f['cve'], 17) + pad(f['sev'], 10) + pad(f['package'], 18) + pad(f['version'], 10)
              + pad(f['fixed'], 26) + ('Y' if f['reachable'] else 'N'))
            note = ''
            if f['gate'] != 'block':
                note = '  (gate: warn — 집계 제외)'
            elif reach_only and not f['reachable']:
                note = '  (미도달 — 집계 제외)'
            p(f'  - 위치: {f["path"]}:{f["line"]}{note}')
    else:
        p(f'  탐지 없음 (CVE 규칙 {len(rules) - n_mois_rules}개 적용)')
    p()
    p('[3] 경고')
    p(RULE)
    for ns, found in ctx['lockfiles'].items():
        if not found:
            n = sum(ns in r['namespaces'] for r in rules)
            hint = LOCKFILE_HINT.get(ns, f'{", ".join(LOCKFILES[ns])} 없음')
            p(f'  - 의존성 파일 미발견: {ECOSYSTEM[ns]} ({hint}) → {ECOSYSTEM[ns]} CVE 규칙 {n}개 미적용')
    if ctx['tag'] == 'untagged':
        p('  - 규칙셋이 태그로 고정되지 않은 커밋에서 실행됨')
    skipped = res.get('skipped_rules') or []
    if skipped:
        p(f'  - Semgrep 이 건너뛴 규칙 {len(skipped)}개: {skipped}')
    p(f'  - Semgrep 파싱 오류 {len(errors)}건')
    for e in errors:
        where = e.get('path') or (e.get('spans') or [{}])[0].get('file') or '-'
        p(f'      [{e.get("level", "?")}] {where}: {" ".join(str(e.get("message", "")).split())[:200]}')
    p()
    p('[4] 게이트 기준 (허용 -1 = 무제한, 보고만)')
    p(RULE)
    p(' ' + pad('항목', 16) + pad('허용', 8, True) + pad('실제', 8, True) + '  판정')
    for label, k in GATE_ROWS:
        verdict = '-' if lim[k] == -1 else ('초과' if count[k] > lim[k] else '통과')
        p(' ' + pad(label, 16) + pad('무제한' if lim[k] == -1 else lim[k], 8, True) + pad(count[k], 8, True)
          + '  ' + verdict)
    p(' ' + pad('Semgrep 오류', 16) + pad(0, 8, True) + pad(len(errors), 8, True) + '  ' + ('초과' if errors else '통과'))
    if reach_only:
        p('  (CVE_REACHABLE_ONLY=true: 도달 가능한 CVE 만 집계)')
    p()
    p(LINE)
    p(f' GATE : {gate}' + ('  (' + ', '.join(f'{label} {n}건' for label, n in over) + ')' if over else ''))
    p(LINE)

    results_dir = env.get('RESULTS_DIR')
    if results_dir:
        for name, value in (('mois-findings', len(mois)), ('cve-findings', len(cve)), ('cve-reachable', reach),
                            ('gate', gate), ('ruleset-version', ctx['ruleset'])):
            Path(results_dir, name).write_text(str(value))
    return 1 if over else 0


if __name__ == '__main__':
    cmd = sys.argv[1:2]
    if cmd == ['check-rules'] and len(sys.argv) == 3:
        sys.exit(check_rules(sys.argv[2]))
    if cmd == ['preflight']:
        sys.exit(preflight())
    if cmd == ['report']:
        sys.exit(report())
    sys.exit(__doc__)
