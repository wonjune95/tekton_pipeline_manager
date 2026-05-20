import os
import re
import subprocess as _sp
import inquirer as _inquirer

# RFC 1123 DNS label: 소문자/숫자로 시작·끝, 가운데에만 하이픈 허용
_K8S_NAME_RE = re.compile(r'^[a-z0-9]([a-z0-9-]*[a-z0-9])?$')

def validate_k8s_name(name: str, label: str) -> str:
    """
    Kubernetes 리소스명 검증 (RFC 1123 DNS label). 문제가 있으면 에러 메시지 반환, 정상이면 ''.
    - 소문자·숫자·하이픈만 허용
    - 소문자/숫자로 시작 및 종료 (하이픈 시작/종료 금지)
    - 최대 53자 (namespace에 '-cicd' suffix 가 붙는 여유분)
    """
    if not name:
        return f'{label}을(를) 입력해주세요.'
    if re.search('[가-힣]', name):
        return f'{label}에 한글은 사용할 수 없습니다.'
    if not _K8S_NAME_RE.match(name):
        return f'{label}는 소문자·숫자·하이픈(-)만 허용되며, 소문자 또는 숫자로 시작·종료해야 합니다.'
    if len(name) > 53:
        return f'{label}는 53자 이하여야 합니다(-cicd suffix 여유분).'
    return ''

# ── 색상 ────────────────────────────────────────────────
C = '\033[96m'    # cyan      — 박스 테두리
Y = '\033[93m'    # yellow    — 메뉴 번호
W = '\033[1;97m'  # bold white — 메뉴 이름
G = '\033[2;37m'  # dim gray  — 설명 / 노트
T = '\033[1;96m'  # bold cyan — 타이틀
R = '\033[0m'     # reset

_N = 64           # 박스 내부 너비 (visual columns)


def _visual_len(s: str) -> int:
    """한글/CJK 2cols, ASCII 1col 기준 시각적 너비."""
    n = 0
    for ch in s:
        n += 2 if '가' <= ch <= '힣' or '一' <= ch <= '鿿' else 1
    return n


def _wrap_text(text: str, max_v: int) -> list:
    """단어 단위 줄바꿈. 한글 2cols 기준으로 max_v 이내로 분할."""
    words = text.split(' ')
    lines, current, current_v = [], '', 0
    for word in words:
        wv = _visual_len(word)
        if current and current_v + 1 + wv > max_v:
            lines.append(current)
            current, current_v = word, wv
        else:
            if current:
                current += ' '
                current_v += 1
            current += word
            current_v += wv
    if current:
        lines.append(current)
    return lines or ['']


def _hline(content: str, content_v: int) -> str:
    """ANSI 포함 content + 시각적 너비(content_v)로 오른쪽 정렬 박스 라인 반환."""
    return f'  {C}║{R}{content}{" " * (_N - content_v)}{C}║{R}'


def draw_menu(title: str, title_v: int, items: list, notes: list = None):
    """
    공통 메뉴 박스 렌더링.

    title / title_v : 헤더 타이틀과 시각적 너비 (한글 2cols, ASCII 1col)
    items : list of dict {
        key    : str  — 입력 키 ('1'~'9')
        name   : str  — 메뉴명
        name_v : int  — name 시각적 너비
        name_w : int  — 이름 컬럼 고정 너비 (없으면 name_v 사용)
        desc   : str  — 설명 (optional, ASCII 권장)
        desc_v : int  — desc 시각적 너비 (optional)
    }
    notes : list of str — 안내 문구 (Korean 포함 가능, 오른쪽 정렬 없음)
    """
    os.system('clear')
    SEP = '═' * _N

    print()
    print(f'  {C}╔{SEP}╗{R}')
    print(f'  {C}║{" " * _N}║{R}')
    print(_hline(f'  {T}{title}{R}', 2 + title_v))
    print(f'  {C}║{" " * _N}║{R}')
    print(f'  {C}╠{SEP}╣{R}')

    if notes:
        print()
        _max_note = _N - 4  # 60 visual cols (2좌측 여백 + 2우측 여백)
        for note in notes:
            for line in _wrap_text(note, _max_note):
                vlen = _visual_len(line)
                print(f'  {C}║  {G}{line}{R}{" " * (_max_note - vlen)}{C}║{R}')
        print()
        print(f'  {C}╠{SEP}╣{R}')

    print(f'  {C}║{" " * _N}║{R}')
    for item in items:
        key    = item['key']
        name   = item['name']
        name_v = item['name_v']
        name_w = item.get('name_w', name_v)
        desc   = item.get('desc', '')
        desc_v = item.get('desc_v', 0)
        pad    = name_w - name_v
        if desc:
            cv = 9 + name_w + desc_v    # "  [ k ]  " = 9 visual
            print(_hline(
                f'  {Y}[ {key} ]{R}  {W}{name}{R}{" " * pad}{G}{desc}{R}',
                cv
            ))
        else:
            print(_hline(
                f'  {Y}[ {key} ]{R}  {W}{name}{R}',
                9 + name_v
            ))

    print(f'  {C}║{" " * _N}║{R}')
    print(f'  {C}╚{SEP}╝{R}')
    print()


def safe_prompt(questions):
    """inquirer.prompt 래퍼: 선택 후 터미널 상태(echo 등) 복원."""
    result = _inquirer.prompt(questions)
    try:
        _sp.run(['stty', 'sane'], capture_output=True, timeout=1)
    except Exception:
        pass
    return result
