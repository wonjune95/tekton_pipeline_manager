#!/usr/bin/env bash
# 규칙 회귀시험. semgrep 이미지 안에서 네트워크 없이 돌린다.
#
#   docker run --rm --network none -v "$PWD":/src -w /src <semgrep 이미지> bash scripts/test.sh
#
#   [1] 규칙 메타데이터
#   [2] 규칙별 fixture: 표시한 줄(ruleid 주석)과 탐지 위치가 정확히 일치, patched 0건, semgrep errors 0
#   [2b] 모든 patched fixture 를 모든 규칙으로 스캔해 0건
#   [3] Task 흐름(preflight → scan → report) 시나리오: 게이트 판정과 preflight 실패 조건
# 하나라도 실패하면 종료코드 1. 태그는 이 시험을 통과한 커밋에만 붙인다.
set -euo pipefail
cd "$(dirname "$0")/.."
ROOT=$PWD
W=$(mktemp -d)
trap 'rm -rf "$W"' EXIT
# 작업공간 소유자(uid)가 달라도 git 이 저장소를 읽게 한다 (Task 와 같은 설정)
export GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory GIT_CONFIG_VALUE_0='*'
failed=0
ok()  { echo "  ok   $*"; }
bad() { echo "  FAIL $*"; failed=$((failed + 1)); }

echo "[1] 규칙 메타데이터"
if python3 scripts/report.py check-rules rules > "$W/rules.json"; then
  ok "규칙 $(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["count"])' "$W/rules.json")개"
else
  bad "메타데이터 검사"
  echo; echo "실패 ${failed}건"; exit 1
fi

echo "[2] 규칙별 fixture (표시한 줄과 탐지 위치가 정확히 일치해야 한다)"
python3 -c 'import json,sys; [print(r["id"], r["file"], sep="\t") for r in json.load(open(sys.argv[1]))["rules"]]' \
  "$W/rules.json" > "$W/ids"
while IFS=$'\t' read -r id file; do
  for c in vulnerable patched; do
    d="fixtures/$id/$c"
    if [ ! -d "$d" ]; then bad "$id: $d 없음"; continue; fi
    if ! (cd "$d" && semgrep scan --config "$ROOT/$file" --metrics=off --disable-version-check \
          --json -o "$W/o.json" . >/dev/null 2>"$W/err"); then
      bad "$id/$c: semgrep 실행 오류"; sed 's/^/       /' "$W/err" | tail -5; continue
    fi
    if out=$(python3 scripts/expect.py "$W/o.json" "$id" "$d"); then
      n=$(printf '%s\n' "$out" | tail -1)
      if [ "$c" = vulnerable ] && [ "$n" = 0 ]; then
        bad "$id/vulnerable: 표시한 탐지 위치가 없음 — 규칙마다 반드시 탐지되는 예제가 있어야 한다"
      else
        ok "$id/$c: ${n}건"
      fi
    else
      bad "$id/$c: 기대 위치와 다름"; printf '%s\n' "$out" | sed '$d'
    fi
  done
done < "$W/ids"
# (cut | grep -q 는 pipefail 에서 grep 이 먼저 끝나면 SIGPIPE 로 실패하므로 파일로 받아 비교한다)
cut -f1 "$W/ids" > "$W/idlist"
for d in fixtures/*/; do
  id=$(basename "$d")
  grep -qxF -- "$id" "$W/idlist" || bad "fixtures/$id: 같은 id 의 규칙 없음"
done

echo "[2b] 모든 patched fixture × 모든 규칙 = 0건"
if semgrep scan --config "$ROOT/rules" --metrics=off --disable-version-check --json -o "$W/all.json" \
     fixtures/*/patched >/dev/null 2>"$W/err"; then
  if python3 - "$W/all.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
for e in d['errors']:
    print('       semgrep error:', e.get('message', '')[:200])
for r in d['results']:
    print(f"       {r['check_id'].rsplit('.', 1)[-1]}  {r['path']}:{r['start']['line']}")
sys.exit(1 if d['errors'] or d['results'] else 0)
PY
  then ok "교차 탐지 0건"; else bad "patched fixture 가 다른 규칙에 걸림"; fi
else
  bad "교차 검사: semgrep 실행 오류"; sed 's/^/       /' "$W/err" | tail -5
fi

echo "[3] Task 흐름 시나리오"
mkdir -p "$W/vuln" "$W/safe" "$W/nolock" "$W/unreach" "$W/empty-rules/rules"
for d in fixtures/*/; do
  id=$(basename "$d"); cp -r "$d/vulnerable" "$W/vuln/$id"; cp -r "$d/patched" "$W/safe/$id"
done
cp -r fixtures/mois-1-01-sql-injection-jdbc/vulnerable/. "$W/nolock/"                  # 의존성 파일 없음, 행안부 block NB 건
NB=$(grep -rhoE "ruleid: " "$W/nolock" | wc -l)                                        # 표시한 줄 수 = block 건수 ([2] 에서 확인됨)
cp fixtures/cve-2021-44228-log4j-core/vulnerable/maven_dep_tree.txt "$W/unreach/"     # 취약 버전, 호출 없음
ln -s "$ROOT/scripts" "$W/empty-rules/scripts"
# main 에 2건, feature 에서 1건 추가
g="$W/git"; mkdir -p "$g"
cp fixtures/mois-1-01-sql-injection-jdbc/vulnerable/UserDao.java "$g/"
git -C "$g" init -q -b main && git -C "$g" add . && git -C "$g" -c user.name=t -c user.email=t@t commit -qm base
git -C "$g" checkout -qb feature
cp fixtures/mois-1-01-sql-injection-jdbc/vulnerable/OrderDao.java "$g/"
git -C "$g" add . && git -C "$g" -c user.name=t -c user.email=t@t commit -qm feature

# Task 의 step 순서 그대로 실행. 출력은 $W/log
run_task() {
  local target=$1; shift
  rm -rf "$W/out"; mkdir -p "$W/out"
  (
    export RULES_ROOT=$ROOT RULES_PATH=rules SRC_ROOT=$target TARGET_PATH=. OUT_DIR=$W/out \
      MAX_MOIS_BLOCK=0 MAX_MOIS_WARN=-1 MAX_CVE_CRITICAL=0 MAX_CVE_HIGH=0 MAX_CVE_MEDIUM=-1 \
      CVE_REACHABLE_ONLY=false BASELINE_REF= TIMEOUT_SEC=300
    [ $# -eq 0 ] || export "$@"
    python3 "$RULES_ROOT/scripts/report.py" preflight || exit $?
    cd "$SRC_ROOT/$TARGET_PATH"
    args=(--config "$RULES_ROOT/$RULES_PATH" --metrics=off --disable-version-check --json -o "$OUT_DIR/semgrep.json")
    [ -z "$BASELINE_REF" ] || args+=(--baseline-commit "$BASELINE_REF")
    timeout "$TIMEOUT_SEC" semgrep scan "${args[@]}" . >/dev/null 2>&1 || exit $?
    python3 "$RULES_ROOT/scripts/report.py" report
  ) > "$W/log" 2>&1
}
# expect <이름> <기대 종료코드> <출력에 있어야 할 문구> <대상> [변수=값 ...]
expect() {
  local name=$1 want=$2 text=$3; shift 3
  local rc=0
  run_task "$@" || rc=$?
  if [ "$rc" = "$want" ] && grep -qF -- "$text" "$W/log"; then
    ok "$name"
  else
    bad "$name — 종료코드 $rc (기대 $want), 문구 '$text'"; sed 's/^/       | /' "$W/log" | tail -30
  fi
}
expect "취약 fixture → FAIL"                          1 "GATE : FAIL"        "$W/vuln"
expect "안전 fixture → PASS, 0건 명시"                 0 "총 0건"             "$W/safe"
expect "RULES_PATH=p/default → preflight 실패"        1 "원격 설정"          "$W/safe"    RULES_PATH=p/default
expect "빈 규칙 디렉터리 → preflight 실패"              1 "규칙 0개"           "$W/safe"    RULES_ROOT="$W/empty-rules"
expect "의존성 파일 없음 → 경고"                       0 "의존성 파일 미발견"  "$W/nolock"  MAX_MOIS_BLOCK=-1
expect "탐지 ${NB}건, MAX_MOIS_BLOCK=${NB} → PASS"            0 "GATE : PASS"        "$W/nolock"  MAX_MOIS_BLOCK=$NB
expect "탐지 ${NB}건, MAX_MOIS_BLOCK=$((NB - 1)) → FAIL, 기준치 표"  1 "초과"               "$W/nolock"  MAX_MOIS_BLOCK=$((NB - 1))
expect "MAX_CVE_HIGH=abc → preflight 실패"            1 "MAX_CVE_HIGH"       "$W/safe"    MAX_CVE_HIGH=abc
expect "미도달 CVE, 전체 집계 → FAIL"                  1 "GATE : FAIL"        "$W/unreach"
expect "미도달 CVE, CVE_REACHABLE_ONLY=true → PASS"   0 "GATE : PASS"        "$W/unreach" CVE_REACHABLE_ONLY=true
expect "feature + BASELINE_REF=main → 신규 1건만"      0 "점검 범위: 신규"     "$g"         BASELINE_REF=main MAX_MOIS_BLOCK=1
expect "BASELINE_REF 기준 커밋 없음 → preflight 실패"  1 "기준 커밋"          "$g"         BASELINE_REF=release

echo
if [ "$failed" -eq 0 ]; then echo "전체 통과"; else echo "실패 ${failed}건"; exit 1; fi
