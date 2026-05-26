#!/bin/bash
# ════════════════════════════════════════════════════════════════
#  통합 오프라인 설치 스크립트 (폐쇄망용)
#
#  지원 OS:
#    Rocky Linux  8 / 9 / 10
#    Ubuntu      22.04 / 24.04 / 26.04
#
#  실행 방법: sudo ./install.sh
#
#  디렉토리 구조:
#    rocky/
#      packages/          ← Python wheel (Rocky 공통)
#        rocky{8|9|10}/   ← 버전별 wheel (있으면 우선)
#      rpms/
#        rocky8/          ← Rocky 8 시스템 패키지 (.rpm)
#        rocky9/          ← Rocky 9 시스템 패키지 (.rpm)
#        rocky10/         ← Rocky 10 시스템 패키지 (.rpm)
#    ubuntu/
#      packages/          ← Python wheel (Ubuntu 공통)
#        ubuntu{22|24|26}/ ← 버전별 wheel (있으면 우선)
#      debs/
#        ubuntu22/        ← Ubuntu 22.04 시스템 패키지 (.deb)
#        ubuntu24/        ← Ubuntu 24.04 시스템 패키지 (.deb)
#        ubuntu26/        ← Ubuntu 26.04 시스템 패키지 (.deb)
# ════════════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REQ_FILE="$SCRIPT_DIR/requirements.txt"

OS_TYPE=""
OS_VER=""
PYTHON=""
pretty=""

# ── OS 감지 ──────────────────────────────────────────────────
detect_os() {
    if [ -f /etc/rocky-release ]; then
        OS_TYPE="rocky"
        OS_VER=$(grep -oP '(?<=release )\d+' /etc/rocky-release 2>/dev/null | head -1 || echo "9")
    elif [ -f /etc/redhat-release ] && grep -qi "rocky" /etc/redhat-release 2>/dev/null; then
        OS_TYPE="rocky"
        OS_VER=$(grep -oP '(?<=release )\d+' /etc/redhat-release 2>/dev/null | head -1 || echo "9")
    elif [ -f /etc/os-release ]; then
        local os_id
        os_id=$(grep '^ID=' /etc/os-release | cut -d'=' -f2 | tr -d '"')
        case "$os_id" in
            ubuntu)
                OS_TYPE="ubuntu"
                local ver
                ver=$(grep '^VERSION_ID=' /etc/os-release | cut -d'=' -f2 | tr -d '"')
                OS_VER=$(echo "$ver" | cut -d'.' -f1)  # "22.04" → "22"
                ;;
            *)
                echo "[ERROR] 지원하지 않는 OS입니다: $os_id"
                echo "        지원 OS: Rocky Linux 8/9/10, Ubuntu 22.04/24.04/26.04"
                exit 1
                ;;
        esac
    else
        echo "[ERROR] OS 정보를 확인할 수 없습니다 (/etc/os-release 없음)."
        exit 1
    fi
}

# ── Python 인터프리터 선택 ────────────────────────────────────
select_python() {
    local candidates=()

    case "$OS_TYPE:$OS_VER" in
        rocky:8)  candidates=(python3.9 python39 python3.8 python38 python3) ;;
        rocky:9)  candidates=(python3.11 python3.10 python3.9 python39 python3) ;;
        rocky:10) candidates=(python3.12 python3.11 python3.10 python3) ;;
        ubuntu:22) candidates=(python3.10 python3.11 python3) ;;
        ubuntu:24) candidates=(python3.12 python3.11 python3) ;;
        ubuntu:26) candidates=(python3.13 python3.12 python3) ;;
        *)         candidates=(python3.13 python3.12 python3.11 python3.10 python3.9 python3) ;;
    esac

    for candidate in "${candidates[@]}"; do
        if command -v "$candidate" &>/dev/null; then
            local minor
            minor=$("$candidate" --version 2>&1 | grep -oP '(?<=Python 3\.)\d+' || echo 0)
            if [ "${minor:-0}" -ge 8 ]; then
                PYTHON="$candidate"
                return
            fi
        fi
    done

    echo "[ERROR] Python 3.8 이상을 찾을 수 없습니다."
    case "$OS_TYPE:$OS_VER" in
        rocky:8)  echo "        sudo dnf install -y python39 python39-pip" ;;
        rocky:*)  echo "        sudo dnf install -y python3 python3-pip" ;;
        ubuntu:*) echo "        sudo apt-get install -y python3 python3-pip" ;;
    esac
    exit 1
}

# ── Rocky: 시스템 패키지 설치 (.rpm) ─────────────────────────
install_rocky_system_pkgs() {
    local rpm_dir="$SCRIPT_DIR/rocky/rpms/rocky${OS_VER}"

    echo "[1/2] 시스템 패키지 설치 (rocky/rpms/rocky${OS_VER}/) ..."

    if [ ! -d "$rpm_dir" ]; then
        echo "      [WARN] $rpm_dir 폴더가 없습니다 — 시스템 패키지 건너뜀"
        echo "             download.sh를 Rocky Linux ${OS_VER} 환경에서 실행 후 rpm 파일을 추가하세요."
        return
    fi

    local rpm_count
    rpm_count=$(find "$rpm_dir" -maxdepth 1 -name '*.rpm' 2>/dev/null | wc -l)

    if [ "$rpm_count" -eq 0 ]; then
        echo "      [WARN] rocky${OS_VER}/ 폴더가 비어 있습니다 — 시스템 패키지 건너뜀"
        echo "             download.sh를 Rocky Linux ${OS_VER} 환경에서 실행하여 .rpm 파일을 채우세요."
        return
    fi

    echo "      경로 : $rpm_dir ($rpm_count개)"
    local dnf_cmd
    dnf_cmd=$(command -v dnf5 2>/dev/null || command -v dnf 2>/dev/null || true)
    if [ -n "$dnf_cmd" ] && [[ "$(basename "$dnf_cmd")" = "dnf5" ]]; then
        "$dnf_cmd" install -y --disablerepo='*' "$rpm_dir"/*.rpm 2>/dev/null || \
        rpm -Uvh --replacepkgs --nodeps "$rpm_dir"/*.rpm 2>/dev/null || true
    else
        dnf localinstall -y --disablerepo='*' "$rpm_dir"/*.rpm 2>/dev/null || \
        rpm -Uvh --replacepkgs --nodeps "$rpm_dir"/*.rpm 2>/dev/null || true
    fi

    echo "      git   : $(git --version 2>/dev/null || echo '확인 필요')"
    echo "      python: $(python3 --version 2>/dev/null || echo '확인 필요')"
}

# ── Ubuntu: 시스템 패키지 설치 (.deb) ────────────────────────
install_ubuntu_system_pkgs() {
    local deb_dir="$SCRIPT_DIR/ubuntu/debs/ubuntu${OS_VER}"

    echo "[1/2] 시스템 패키지 설치 (ubuntu/debs/ubuntu${OS_VER}/) ..."

    if [ ! -d "$deb_dir" ]; then
        echo "      [WARN] $deb_dir 폴더가 없습니다 — 시스템 패키지 건너뜀"
        echo "             download.sh를 Ubuntu ${OS_VER}.04 환경에서 실행 후 deb 파일을 추가하세요."
        return
    fi

    local deb_count
    deb_count=$(find "$deb_dir" -maxdepth 1 -name '*.deb' 2>/dev/null | wc -l)

    if [ "$deb_count" -eq 0 ]; then
        echo "      [WARN] ubuntu${OS_VER}/ 폴더가 비어 있습니다 — 시스템 패키지 건너뜀"
        echo "             download.sh를 Ubuntu ${OS_VER}.04 환경에서 실행하여 .deb 파일을 채우세요."
        return
    fi

    echo "      경로 : $deb_dir ($deb_count개)"
    dpkg -i "$deb_dir"/*.deb 2>/dev/null || true
    apt-get install -f -y 2>/dev/null || true

    echo "      git   : $(git --version 2>/dev/null || echo '확인 필요')"
    echo "      python: $(python3 --version 2>/dev/null || echo '확인 필요')"
    echo "      pip   : $(python3 -m pip --version 2>/dev/null | cut -d' ' -f1-2 || echo '확인 필요')"
}

# ── Python 패키지 설치 (오프라인 wheel) ──────────────────────
install_python_pkgs() {
    echo ""
    echo "[2/2] Python 패키지 오프라인 설치 ..."

    # 버전별 디렉토리 우선, 없으면 공통 디렉토리 fallback
    local versioned_dir common_dir PY_PKG_DIR

    case "$OS_TYPE" in
        rocky)
            versioned_dir="$SCRIPT_DIR/rocky/packages/rocky${OS_VER}"
            common_dir="$SCRIPT_DIR/rocky/packages"
            ;;
        ubuntu)
            versioned_dir="$SCRIPT_DIR/ubuntu/packages/ubuntu${OS_VER}"
            common_dir="$SCRIPT_DIR/ubuntu/packages"
            ;;
    esac

    if [ -d "$versioned_dir" ] && [ -n "$(find "$versioned_dir" -maxdepth 1 -name '*.whl' 2>/dev/null | head -1)" ]; then
        PY_PKG_DIR="$versioned_dir"
    elif [ -d "$common_dir" ] && [ -n "$(find "$common_dir" -maxdepth 1 -name '*.whl' 2>/dev/null | head -1)" ]; then
        PY_PKG_DIR="$common_dir"
    else
        echo "[ERROR] Python wheel 파일을 찾을 수 없습니다."
        echo "        download.sh를 실행하여 packages/ 폴더를 채우세요."
        exit 1
    fi

    local py_ver
    py_ver=$("$PYTHON" --version 2>&1)
    echo "      Python: $py_ver"
    echo "      경로  : $PY_PKG_DIR"

    # Python 버전과 wheel 호환성 경고
    local py_minor
    py_minor=$("$PYTHON" --version 2>&1 | grep -oP '(?<=Python 3\.)\d+' || echo 0)
    if [ "$OS_TYPE" = "rocky" ] && [ "$OS_VER" -ge 10 ] && [ "${py_minor:-0}" -ge 12 ]; then
        if [ "$PY_PKG_DIR" = "$common_dir" ]; then
            echo "      [WARN] Python 3.${py_minor} 환경에서 Rocky 공통 wheel(cp39)을 사용합니다."
            echo "             일부 패키지가 실패할 경우 rocky/packages/rocky10/ 에"
            echo "             Python 3.${py_minor}용 wheel을 별도 추가하세요."
        fi
    fi
    if [ "$OS_TYPE" = "ubuntu" ] && [ "$OS_VER" -ge 24 ] && [ "${py_minor:-0}" -ge 12 ]; then
        if [ "$PY_PKG_DIR" = "$common_dir" ]; then
            echo "      [WARN] Python 3.${py_minor} 환경에서 Ubuntu 공통 wheel(cp310)을 사용합니다."
            echo "             일부 패키지가 실패할 경우 ubuntu/packages/ubuntu${OS_VER}/ 에"
            echo "             Python 3.${py_minor}용 wheel을 별도 추가하세요."
        fi
    fi

    "$PYTHON" -m pip install \
        --no-index \
        --find-links "$PY_PKG_DIR" \
        -r "$REQ_FILE"
}

# ── 결과 출력 ────────────────────────────────────────────────
show_result() {
    echo ""
    echo "════════════════════════════════════════════════"
    echo "  설치 완료"
    echo "════════════════════════════════════════════════"
    "$PYTHON" -m pip list 2>/dev/null | grep -iE \
        "tomli|jinja2|inquirer|paramiko|pexpect|requests|cryptography|blessed|bcrypt|pynacl|cffi" \
        | awk '{printf "  %-30s %s\n", $1, $2}'
    echo ""
    echo "  git: $(git --version 2>/dev/null || echo '미설치')"
    echo "════════════════════════════════════════════════"
}

# ════════════════════════════════════════════════════════════
#  메인
# ════════════════════════════════════════════════════════════
detect_os

echo "════════════════════════════════════════════════"
echo "  오프라인 설치 (통합 스크립트)"
echo "════════════════════════════════════════════════"

case "$OS_TYPE" in
    rocky)
        echo "  OS: Rocky Linux ${OS_VER} ($(cat /etc/rocky-release 2>/dev/null || cat /etc/redhat-release 2>/dev/null | head -1))"
        echo ""
        install_rocky_system_pkgs
        ;;
    ubuntu)
        pretty=$(grep '^PRETTY_NAME=' /etc/os-release | cut -d'=' -f2 | tr -d '"')
        echo "  OS: Ubuntu ${OS_VER}.04 ($pretty)"
        echo ""
        install_ubuntu_system_pkgs
        ;;
esac

select_python

if ! "$PYTHON" -m pip --version &>/dev/null; then
    echo "[ERROR] pip를 찾을 수 없습니다."
    case "$OS_TYPE:$OS_VER" in
        rocky:8)  echo "        sudo dnf install -y python39-pip" ;;
        rocky:*)  echo "        sudo dnf install -y python3-pip" ;;
        ubuntu:*) echo "        sudo apt-get install -y python3-pip" ;;
    esac
    exit 1
fi

install_python_pkgs
show_result
