import os

# ── 색상 ────────────────────────────────────────────────
C = '\033[96m'    # cyan      — 박스 테두리
Y = '\033[93m'    # yellow    — 메뉴 번호
W = '\033[1;97m'  # bold white — 메뉴 이름
G = '\033[2;37m'  # dim gray  — 설명 / 노트
T = '\033[1;96m'  # bold cyan — 타이틀
R = '\033[0m'     # reset

_N = 64           # 박스 내부 너비 (visual columns)


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
        for note in notes:
            print(f'  {C}║  {G}{note}{R}')
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
