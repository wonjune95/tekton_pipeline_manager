#!/bin/bash
# ════════════════════════════════════════════════════════════════
#  Rocky Linux 패키지 다운로드 스크립트
# ════════════════════════════════════════════════════════════════
#  !! 반드시 인터넷이 연결된 Rocky Linux 머신에서 실행 !!
#     Ubuntu/WSL 등 다른 OS에서 실행하면 안 됩니다.
#
#  이유 : Python 바이너리 휠이 OS별 glibc 버전에 따라 달라짐
#         Rocky 8 (glibc 2.28) / Rocky 9 (glibc 2.34) / Rocky 10 (glibc 2.39+)
#
#  실행 환경 : 인터넷 연결된 Rocky Linux 머신
#              (폐쇄망 대상과 동일한 Rocky 버전 / x86_64)
#              Rocky  8 : Python 3.9 권장  (python39, python39-pip)
#              Rocky  9 : Python 3.9 이상  (python3, python3-pip)
#              Rocky 10 : Python 3.12 이상 (python3, python3-pip) / dnf5 사용
#
#  다운로드 결과 :
#    packages/  ─ Python wheel (.whl) 파일
#    rpms/      ─ git, python3, python3-pip .rpm 패키지 및 의존성
#
#  다음 단계 :
#    rocky/ 폴더 전체를 폐쇄망으로 복사 후 install.sh 실행
# ════════════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REQ_FILE="$SCRIPT_DIR/../requirements.txt"

echo "════════════════════════════════════════════════"
echo "  Rocky Linux 패키지 다운로드"
echo "════════════════════════════════════════════════"
echo "  OS    : $(cat /etc/rocky-release 2>/dev/null || cat /etc/redhat-release 2>/dev/null || echo '확인불가')"
echo "  아키텍처: $(uname -m)"
echo ""

# ── Rocky 버전 감지 ──────────────────────────────────
ROCKY_VER=9
if [ -f /etc/rocky-release ]; then
    ROCKY_VER=$(grep -oP '(?<=release )\d+' /etc/rocky-release 2>/dev/null | head -1 || echo 9)
elif [ -f /etc/redhat-release ]; then
    ROCKY_VER=$(grep -oP '(?<=release )\d+' /etc/redhat-release 2>/dev/null | head -1 || echo 9)
fi
echo "[INFO] Rocky 버전: $ROCKY_VER"

# install.sh 가 rpms/rocky${VER}/, packages/rocky${VER}/ 경로를 찾으므로 동일 위치에 저장
RPM_DIR="$SCRIPT_DIR/rpms/rocky${ROCKY_VER}"
PY_PKG_DIR="$SCRIPT_DIR/packages/rocky${ROCKY_VER}"

# ── dnf5 (Rocky 10+) 또는 dnf (Rocky 8/9) 선택 ──────
DNF=$(command -v dnf5 2>/dev/null || command -v dnf 2>/dev/null || true)
if [ -z "$DNF" ]; then
    echo "[ERROR] dnf 또는 dnf5를 찾을 수 없습니다."
    exit 1
fi
echo "[INFO] 패키지 매니저: $(basename "$DNF")"

# ── Python 선택 (3.9 이상 우선) ──────────────────────
PYTHON=""
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
    if [ "$ROCKY_VER" = "8" ]; then
        echo "        sudo $DNF install -y python39 python39-pip"
    else
        echo "        sudo $DNF install -y python3 python3-pip"
    fi
    exit 1
fi
echo "[INFO] Python: $($PYTHON --version)"

if ! $PYTHON -m pip --version &>/dev/null; then
    echo "[ERROR] pip가 없습니다."
    if [ "$ROCKY_VER" = "8" ]; then
        echo "        sudo $DNF install -y python39-pip"
    else
        echo "        sudo $DNF install -y python3-pip"
    fi
    exit 1
fi

# ── dnf-plugins-core 확인 (dnf 전용, dnf5는 download 내장) ──
if [[ "$(basename "$DNF")" != "dnf5" ]] && ! "$DNF" download --help &>/dev/null 2>&1; then
    echo "[INFO] dnf-plugins-core 설치 중 ..."
    sudo "$DNF" install -y dnf-plugins-core
fi

# ── [1/2] Python 패키지 다운로드 ─────────────────────
mkdir -p "$PY_PKG_DIR"
echo ""
echo "[1/2] Python 패키지 다운로드 ..."
echo "      경로: $PY_PKG_DIR (rocky${ROCKY_VER})"

$PYTHON -m pip download \
    -r "$REQ_FILE" \
    -d "$PY_PKG_DIR" \
    --prefer-binary

PY_COUNT=$(ls "$PY_PKG_DIR" | wc -l)
echo "      완료: ${PY_COUNT}개 파일"

# ── [2/2] 시스템 패키지 다운로드 (git + python3-pip) ──
mkdir -p "$RPM_DIR"
echo ""
echo "[2/2] 시스템 패키지 .rpm 다운로드 ..."
echo "      경로: $RPM_DIR"

case "$ROCKY_VER" in
    8)
        # Rocky 8: python39 우선, 없으면 python38, 마지막으로 python3
        sudo "$DNF" download --resolve --destdir="$RPM_DIR" \
            git python39 python39-pip 2>/dev/null || \
        sudo "$DNF" download --resolve --destdir="$RPM_DIR" \
            git python38 python38-pip 2>/dev/null || \
        sudo "$DNF" download --resolve --destdir="$RPM_DIR" \
            git python3 python3-pip
        ;;
    *)
        # Rocky 9 / 10
        sudo "$DNF" download --resolve --destdir="$RPM_DIR" \
            git python3 python3-pip
        ;;
esac

RPM_COUNT=$(ls "$RPM_DIR" 2>/dev/null | wc -l)
echo "      완료: ${RPM_COUNT}개 파일"

# ── 결과 요약 ────────────────────────────────────────
echo ""
echo "════════════════════════════════════════════════"
echo "  다운로드 완료"
echo "════════════════════════════════════════════════"
echo "  Python 패키지 : packages/rocky${ROCKY_VER}/  (${PY_COUNT}개)"
echo "  시스템 패키지 : rpms/rocky${ROCKY_VER}/     (${RPM_COUNT}개)"
echo ""
echo "  [다음 단계]"
echo "  rocky/ 폴더 전체를 폐쇄망 서버에 복사 후:"
echo "    chmod +x install.sh && sudo ./install.sh"
echo "════════════════════════════════════════════════"
