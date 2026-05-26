#!/bin/bash
# ════════════════════════════════════════════════════════════════
#  Rocky Linux 오프라인 설치 스크립트 (폐쇄망용)
# ════════════════════════════════════════════════════════════════
#  실행 전 준비 : rocky/ 폴더 전체가 이 머신에 복사되어 있어야 함
#  실행 방법   : sudo ./install.sh
# ════════════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RPM_BASE="$SCRIPT_DIR/rpms"
REQ_FILE="$SCRIPT_DIR/../requirements.txt"

echo "════════════════════════════════════════════════"
echo "  Rocky Linux 오프라인 설치"
echo "════════════════════════════════════════════════"
echo "  OS    : $(cat /etc/rocky-release 2>/dev/null || cat /etc/redhat-release 2>/dev/null || echo '확인불가')"
echo ""

# ── Rocky 버전 감지 ──────────────────────────────────
ROCKY_VER=9
if [ -f /etc/rocky-release ]; then
    ROCKY_VER=$(grep -oP '(?<=release )\d+' /etc/rocky-release 2>/dev/null | head -1 || echo 9)
elif [ -f /etc/redhat-release ]; then
    ROCKY_VER=$(grep -oP '(?<=release )\d+' /etc/redhat-release 2>/dev/null | head -1 || echo 9)
fi
echo "[INFO] Rocky 버전: $ROCKY_VER"

# ── dnf5 (Rocky 10+) 또는 dnf (Rocky 8/9) 선택 ──────
DNF=$(command -v dnf5 2>/dev/null || command -v dnf 2>/dev/null || true)
if [ -z "$DNF" ]; then
    echo "[WARN] dnf 또는 dnf5를 찾을 수 없습니다. rpm 직접 설치를 시도합니다."
fi

RPM_DIR="$RPM_BASE/rocky${ROCKY_VER}"

# ── [1/2] 시스템 패키지 설치 ─────────────────────────
echo ""
echo "[1/2] 시스템 패키지 설치 (rocky${ROCKY_VER}/) ..."

if [ -d "$RPM_DIR" ] && [ "$(ls -A "$RPM_DIR" 2>/dev/null)" ]; then
    echo "      경로: $RPM_DIR"
    # dnf5 (Rocky 10)는 localinstall 미지원 → install 사용
    if [ -n "$DNF" ] && [[ "$(basename "$DNF")" = "dnf5" ]]; then
        "$DNF" install -y --disablerepo='*' "$RPM_DIR"/*.rpm 2>/dev/null || \
        rpm -Uvh --replacepkgs --nodeps "$RPM_DIR"/*.rpm 2>/dev/null || true
    else
        dnf localinstall -y --disablerepo='*' "$RPM_DIR"/*.rpm 2>/dev/null || \
        rpm -Uvh --replacepkgs --nodeps "$RPM_DIR"/*.rpm 2>/dev/null || true
    fi

    echo "      git    : $(git --version 2>/dev/null || echo '확인 필요')"
    echo "      python : $(python3 --version 2>/dev/null || python3.9 --version 2>/dev/null || echo '확인 필요')"
else
    echo "      [WARN] rpms/rocky${ROCKY_VER}/ 폴더 없음 — 시스템 패키지 건너뜀"
    echo "             git, python3 가 이미 설치되어 있는지 확인하세요."
fi

# ── Python 인터프리터 선택 ────────────────────────────
PYTHON=""
# Rocky 8은 python39/python38 명령어 사용
for CANDIDATE in python3.12 python3.11 python3.10 python3.9 python39 python3.8 python38 python3; do
    if command -v "$CANDIDATE" &>/dev/null; then
        MINOR=$($CANDIDATE --version 2>&1 | grep -oP '(?<=Python 3\.)\d+' || echo 0)
        if [ "${MINOR}" -ge 8 ]; then
            PYTHON="$CANDIDATE"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo "[ERROR] Python 3.8 이상이 없습니다."
    exit 1
fi

if ! $PYTHON -m pip --version &>/dev/null; then
    echo "[ERROR] pip가 없습니다."
    exit 1
fi

# ── [2/2] Python 패키지 설치 (오프라인) ──────────────
echo ""
echo "[2/2] Python 패키지 오프라인 설치 ..."

# 버전별 디렉토리 우선, 없으면 공통 디렉토리 fallback
VERSIONED_PKG="$SCRIPT_DIR/packages/rocky${ROCKY_VER}"
COMMON_PKG="$SCRIPT_DIR/packages"
PY_PKG_DIR=""
if [ -d "$VERSIONED_PKG" ] && [ -n "$(find "$VERSIONED_PKG" -maxdepth 1 -name '*.whl' 2>/dev/null | head -1)" ]; then
    PY_PKG_DIR="$VERSIONED_PKG"
elif [ -d "$COMMON_PKG" ] && [ -n "$(find "$COMMON_PKG" -maxdepth 1 -name '*.whl' 2>/dev/null | head -1)" ]; then
    PY_PKG_DIR="$COMMON_PKG"
else
    echo "[ERROR] packages/ 폴더가 없거나 비어 있습니다."
    echo "        인터넷 연결 환경에서 download.sh 를 먼저 실행하세요."
    exit 1
fi

echo "      Python: $($PYTHON --version)"
echo "      경로  : $PY_PKG_DIR"

$PYTHON -m pip install \
    --no-index \
    --find-links "$PY_PKG_DIR" \
    -r "$REQ_FILE"

# ── 결과 확인 ────────────────────────────────────────
echo ""
echo "════════════════════════════════════════════════"
echo "  설치 완료 — 설치된 패키지"
echo "════════════════════════════════════════════════"
$PYTHON -m pip list 2>/dev/null | grep -iE \
    "tomli|jinja2|inquirer|paramiko|pexpect|requests|cryptography|blessed|bcrypt|pynacl|cffi" \
    | awk '{printf "  %-30s %s\n", $1, $2}'

echo ""
echo "  git: $(git --version 2>/dev/null || echo '미설치')"
echo "════════════════════════════════════════════════"
