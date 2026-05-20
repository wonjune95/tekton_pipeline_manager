import os
import sys
import json
import argparse
import base64
try:
    import tomllib
except ImportError:
    import tomli as tomllib
import warnings

warnings.filterwarnings(action='ignore')

from menu.menu1_init import menu1, validate_config
from menu.menu2_add_org import menu2
from menu.menu3_add_pipeline_runner import menu3
from menu.menu4_add_gitops import menu4
from menu.menu5_reset_cache import menu5

# ======== 환경파일 LOAD 및 인증 정보 생성 ========

def load_env():
    """
    환경변수 파일(tekton_init.toml, tekton.env) 읽고
    인증에 필요한 base64 auth 키 추가
    """
    env = {}
    toml_path = './00.reset/tekton_init.toml'
    if os.path.exists(toml_path):
        try:
            with open(toml_path, 'rb') as f:
                env.update(tomllib.load(f))
        except tomllib.TOMLDecodeError as e:
            print(f'\033[91m[CONFIG ERROR] {toml_path} TOML 문법 오류: {e}\033[0m')
            print('\033[91m  → 따옴표/대괄호/줄바꿈을 확인하세요.\033[0m')
            sys.exit(1)
    env_path = './tekton.env'
    if os.path.exists(env_path):
        try:
            with open(env_path, 'r') as f:
                env.update(json.load(f))
        except json.JSONDecodeError as e:
            print(f'\033[91m[CONFIG ERROR] {env_path} JSON 문법 오류: {e}\033[0m')
            sys.exit(1)
    # 각종 인증정보 base64 자동 추가
    keypairs = [
        ('harbor_id', 'harbor_pw', 'harbor_auth'),
        ('harbor_robot_id', 'harbor_robot_pw', 'harbor_robot_auth'),
        ('harbor_admin_id', 'harbor_admin_pw', 'harbor_admin_auth'),
        ('git_cicd_id', 'git_cicd_pw', 'git_cicd_auth')
    ]
    for id_key, pw_key, result_key in keypairs:
        if id_key in env and pw_key in env:
            s = f"{env[id_key]}:{env[pw_key]}"
            env[result_key] = base64.b64encode(s.encode("utf-8")).decode("utf-8")
    env['node_selector_list'] = [n.strip() for n in str(env.get('node_selector', '')).split(',') if n.strip()]
    return env

data = load_env()

# ======== 메인 메뉴 ========

def print_menu():
    os.system('clear')

    C  = '\033[96m'    # cyan      — 박스 테두리
    Y  = '\033[93m'    # yellow    — 메뉴 번호
    W  = '\033[1;97m'  # bold white — 메뉴 이름
    G  = '\033[2;37m'  # dim gray  — 설명
    T  = '\033[1;96m'  # bold cyan — 타이틀
    R  = '\033[0m'     # reset

    project = data.get('project_name', '-')
    N = 64             # 박스 내부 너비 (visual cols)
    SEP = '═' * N

    # 한글(2cols)/ASCII(1col) 혼용 라인의 시각적 패딩 계산
    # 각 라인의 (content, visual_width) 를 미리 계산
    items = [
        # (번호, 이름, 이름_vcols, 설명, 설명_vcols)
        ('1', '초기화',     6,  'Tekton 인프라 초기 설정',       23),
        ('2', '조직 추가',  9,  '새 조직 및 네임스페이스 생성',  28),
        ('3', '파이프라인', 10, '앱 CI/CD 파이프라인 러너 생성', 29),
        ('4', 'GitOps',     6,  'GitOps 레포 생성 및 초기화',    26),
        ('5', '캐시 초기화',11, '캐시 노드 폴더 초기화',         21),
    ]

    print()
    print(f'  {C}╔{SEP}╗{R}')
    print(f'  {C}║{" " * N}║{R}')
    # "  TEKTON  PIPELINE  MANAGER" = 2+6+2+8+2+7 = 27 visual
    print(f'  {C}║  {T}TEKTON  PIPELINE  MANAGER{R}{" " * (N - 27)}{C}║{R}')
    # 프로젝트: "  project : {name}" — ASCII only
    proj_vis = 12 + len(project)
    print(f'  {C}║  {G}project : {Y}{project}{R}{" " * (N - proj_vis)}{C}║{R}')
    print(f'  {C}║{" " * N}║{R}')
    print(f'  {C}╠{SEP}╣{R}')
    print(f'  {C}║{" " * N}║{R}')

    for num, name, name_v, desc, desc_v in items:
        # "  [ N ]  " = 9 visual,  name + 2 spaces padding,  desc
        label_pad = 12 - name_v          # 이름을 12 visual cols 폭으로 맞춤
        content_v = 9 + name_v + label_pad + desc_v
        right_pad = N - content_v
        print(f'  {C}║  {Y}[ {num} ]{R}  {W}{name}{R}{" " * label_pad}{G}{desc}{R}{" " * right_pad}{C}║{R}')

    print(f'  {C}║{" " * N}║{R}')
    # "  [ 9 ]  종료" = 9 + 4 = 13 visual
    print(f'  {C}║  {Y}[ 9 ]{R}  {W}종료{R}{" " * (N - 13)}{C}║{R}')
    print(f'  {C}║{" " * N}║{R}')
    print(f'  {C}╚{SEP}╝{R}')
    print()

def main():
    """
    메인 CLI 메뉴 및 분기
    """
    parser = argparse.ArgumentParser(
        prog='python yaml_maker.py',
        description='Tekton Pipeline Manager'
    )
    parser.add_argument(
        'menu', nargs='?', type=int, choices=[1, 2, 3, 4, 5],
        metavar='MENU',
        help='메뉴 번호 직접 실행  1:초기화  2:조직추가  3:파이프라인  4:GitOps  5:캐시초기화'
    )
    args = parser.parse_args()

    if not validate_config(data):
        sys.exit(1)

    menu_actions = {
        1: menu1,
        2: menu2,
        3: menu3,
        4: menu4,
        5: menu5,
    }

    if args.menu:
        menu_actions[args.menu]()
        return

    while True:
        print_menu()
        menu_number = input('\033[1;96m[ 메뉴를 선택하세요 ] ▶ \033[0m').strip()
        if not menu_number.isdigit():
            print('\033[31m숫자만 입력 가능합니다. 다시 시도하세요.\033[0m')
            continue
        menu_number = int(menu_number)
        if menu_number in menu_actions:
            menu_actions[menu_number]()
        elif menu_number == 9:
            print('\033[95m프로그램을 종료합니다.\033[0m')
            break
        else:
            print('\033[31m메뉴내의 숫자만 입력 가능합니다. 입력된 값 : {}\033[0m'.format(menu_number))

if __name__ == "__main__":
    main()
