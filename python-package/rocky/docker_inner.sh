#!/bin/bash
# ════════════════════════════════════════════════════════════════
#  컨테이너 내부에서 실행 — 직접 실행하지 마세요
#  download_docker.sh 가 Docker 컨테이너 안에서 호출합니다
# ════════════════════════════════════════════════════════════════

set -euo pipefail

VER="$1"          # 8 or 9
RPM_DIR="/pkg/rocky/rpms/rocky${VER}"
PKG_DIR="/pkg/rocky/packages/rocky${VER}"
REQ_FILE="/pkg/requirements.txt"

mkdir -p "$RPM_DIR" "$PKG_DIR"

# ── [1/2] RPM 다운로드 ──────────────────────────────────────────
echo ""
echo "  [1/2] RPM 다운로드 (rocky${VER}) ..."

dnf install -y dnf-plugins-core

if [ "$VER" = "8" ]; then
    PYTHON_PKGS="python39 python39-pip"
    PYTHON_CMD="python3.9"

    # Rocky 8의 python39는 AppStream 모듈에 있어서 먼저 활성화해야 함
    dnf module enable python39:3.9 -y
else
    PYTHON_PKGS="python3 python3-pip"
    PYTHON_CMD="python3"
fi

# 패키지 본체 먼저 받기 (설치 여부 무관하게 반드시 받음)
dnf download --destdir="$RPM_DIR" git $PYTHON_PKGS || true

# 의존성 전체 받기
dnf download --resolve --destdir="$RPM_DIR" git $PYTHON_PKGS || true

RPM_COUNT=$(ls "$RPM_DIR" 2>/dev/null | wc -l)
echo "      완료: RPM ${RPM_COUNT}개"

# ── [2/2] Python wheel 다운로드 ─────────────────────────────────
echo ""
echo "  [2/2] Python wheel 다운로드 (rocky${VER}) ..."

dnf install -y $PYTHON_PKGS

$PYTHON_CMD -m pip download \
    -r "$REQ_FILE" \
    -d "$PKG_DIR" \
    --prefer-binary

WHL_COUNT=$(ls "$PKG_DIR" 2>/dev/null | wc -l)
echo "      완료: WHL ${WHL_COUNT}개"
