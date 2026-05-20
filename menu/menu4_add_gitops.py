import os
import re
import json
import requests
import inquirer
import subprocess as cmd
from urllib.parse import quote as _urlquote
from jinja2 import Environment, FileSystemLoader
from menu.util import component_api as _cap
from menu.menu1_init import screen_init_value
from menu.util.ui import draw_menu, safe_prompt, validate_k8s_name
from requests.packages.urllib3.exceptions import InsecureRequestWarning

def _pick(*names):
    for n in names:
        if hasattr(_cap, n):
            return getattr(_cap, n)
    return None

# 함수 이름 후보 여러 개를 시도
get_organization   = _pick("get_organization", "get_oragnizaion", "get_organizations")
get_repos_in_orgs  = _pick("get_repos_in_orgs", "get_repos_in_org", "list_repos_in_org")
create_organization = _pick("create_organization", "create_oragnizaion", "ensure_organization")
create_gitops      = _pick("create_gitops", "create_gitops_repo", "ensure_gitops")

# =========================
# 공통 유틸
# =========================
def _print_menu_header():
    draw_menu('4.  GitOps', 10, [
        {'key': '1', 'name': 'tekton_init.toml 값 확인', 'name_v': 24},
        {'key': '2', 'name': '자동선택 모드',             'name_v': 13},
        {'key': '3', 'name': '수동입력 모드',             'name_v': 13},
        {'key': '9', 'name': '뒤로가기',                  'name_v':  8},
    ], notes=[
        '자동선택모드는 gitea와 연동이 되어야 실행 가능합니다.',
        '수동입력모드는 조직명과 어플리케이션명을 직접 입력해야합니다.',
    ])

def _success_or_error(msg: str):
    if not msg:
        return
    if msg == '정상처리':
        print('\033[92m' + msg + '\033[0m')
    else:
        print('\033[91m' + msg + '\033[0m')

def _load_init_json(project_name: str):
    result_path = f'./result/{project_name}'
    init_file = f'{result_path}/{project_name}-init_result.json'
    if not os.path.exists(init_file):
        return None, "초기화 파일이 존재하지 않습니다. 초기화 작업을 먼저 수행해주세요"
    with open(init_file, 'r') as f:
        return json.load(f), ""

def _safe_input_number(prompt: str) -> str:
    v = input(prompt)
    return v if v.isnumeric() else ""

def _select_from_list(title: str, items):
    options = [inquirer.List("option", message=title, choices=items)]
    sel = safe_prompt(options)
    if not sel:
        return None
    return sel['option']

def _is_korean(s: str) -> bool:
    return re.search('[ㄱ-힣]', s) is not None

def _api_base_from_host_url(host_url: str) -> str:
    u = host_url.strip()
    if '://' in u:
        scheme, rest = u.split('://', 1)
    else:
        scheme, rest = 'http', u  # 스킴 없으면 http 기본
    host = rest.split('/')[0]     # 첫 '/' 전까지 host:port
    return f"{scheme}://{host}/gitea/api/v1"

# =========================
# 메뉴
# =========================
def menu4():
    return_string = ''
    while True:
        _print_menu_header()
        _success_or_error(return_string)
        menu_number = input('\033[1;96m[ 메뉴를 선택하세요 ] ▶ \033[0m').strip()
        if not menu_number.isnumeric():
            return_string = '문자는 처리가 되지 않습니다.'
            continue
        n = int(menu_number)
        if n == 1:
            project_name = choice_project()
            if project_name is None:
                return_string = ''
            else:
                init_data, err = _load_init_json(project_name)
                if err:
                    return_string = err
                else:
                    screen_init_value(init_data)
        elif n == 2:
            return_string = add_gitops_execute()
        elif n == 3:
            return_string = manual_mode()
        elif n == 9:
            return ''
        else:
            print('\033[31m' + f'메뉴내의 숫자만 입력가능합니다. 입력된값 : {menu_number}' + '\033[0m')
            continue

# =========================
# 프로젝트 선택
# =========================
def choice_project():
    if not os.path.isdir('result'):
        print('\033[91m초기화된 프로젝트가 없습니다. 메뉴 1에서 초기화를 먼저 실행하세요.\033[0m')
        input('\033[0m계속하려면 엔터를 눌러주세요. ')
        return None
    project_list = [d for d in os.listdir('result') if os.path.isdir(os.path.join('result', d))]
    if not project_list:
        print('\033[91m초기화된 프로젝트가 없습니다. 메뉴 1에서 초기화를 먼저 실행하세요.\033[0m')
        input('\033[0m계속하려면 엔터를 눌러주세요. ')
        return None
    if len(project_list) > 1:
        return _select_from_list("프로젝트를 선택해주세요", project_list)
    return project_list[0]

# =========================
# 자동선택 모드
# =========================
def add_gitops_execute():
    env = {}
    project_name = choice_project()
    if project_name is None:
        return ''
    env['project_name'] = project_name

    init_data, err = _load_init_json(project_name)
    if err:
        return err

    env['gitea_domain'] = init_data['gitea_domain']
    env['git_cicd_auth'] = init_data['git_cicd_auth']

    try:
        org_res = json.loads(get_organization(env))
    except (requests.HTTPError, requests.ConnectionError, ValueError) as e:
        return f"Gitea API 오류 (조직 조회 실패): {e}"
    if len(org_res) == 0:
        return "조직이 존재하지 않습니다. 조직생성후 재실행하시길 바랍니다."

    organization = [o['name'] for o in org_res if 'cicd' not in o['name']]
    if not organization:
        return "조직이 존재하지 않습니다. 조직생성후 재실행하시길 바랍니다."
    env['organization_name'] = _select_from_list("조직명을 선택해주세요", organization)
    if not env['organization_name']:
        return ''

    try:
        app_res = json.loads(get_repos_in_orgs(env))
    except (requests.HTTPError, requests.ConnectionError, ValueError) as e:
        return f"Gitea API 오류 (레포 조회 실패): {e}"
    if len(app_res) == 0:
        return "어플리케이션이 존재하지 않습니다. 어플리케이션생성후 재실행하시길 바랍니다."
    applications = [a['name'] for a in app_res]
    env['application_name'] = _select_from_list("어플리케이션을 선택해주세요", applications)
    if not env['application_name']:
        return ''

    return choice_gitops(env)

# =========================
# 수동입력 모드
# =========================
def manual_mode():
    env = {}
    project_name = choice_project()
    if project_name is None:
        return ''
    env['project_name'] = project_name

    org = input('\033[96m조직명을 입력해주세요(소문자·숫자·하이픈, 예시: sample): \033[0m').strip()
    err = validate_k8s_name(org, '조직명')
    if err:
        return err
    env['organization_name'] = org

    app = input('\033[96m어플리케이션명을 입력해주세요(소문자·숫자·하이픈, 예시: product-frontend): \033[0m').strip()
    err = validate_k8s_name(app, '어플리케이션명')
    if err:
        return err
    env['application_name'] = app

    return choice_gitops(env)

# =========================
# GitOps 타입 선택
# =========================
def choice_gitops(env_dict):
    selection_list = [
        '',
        'frontend-ing',
        'frontend-svc',
        'frontend-hpa-bluegreen',
        'frontend-hpa-canary',
        'backend-ing',
        'backend-svc',
        'backend-hpa-bluegreen',
        'backend-hpa-canary',
    ]
    while True:
        draw_menu('GitOps 유형 선택', 16, [
            {'key': '1', 'name': 'Frontend', 'name_v': 8, 'name_w': 10, 'desc': 'ingress',              'desc_v':  7},
            {'key': '2', 'name': 'Frontend', 'name_v': 8, 'name_w': 10, 'desc': 'service',              'desc_v':  7},
            {'key': '3', 'name': 'Frontend', 'name_v': 8, 'name_w': 10, 'desc': 'ingress - blue/green', 'desc_v': 20},
            {'key': '4', 'name': 'Frontend', 'name_v': 8, 'name_w': 10, 'desc': 'ingress - canary',     'desc_v': 16},
            {'key': '5', 'name': 'Backend',  'name_v': 7, 'name_w': 10, 'desc': 'ingress',              'desc_v':  7},
            {'key': '6', 'name': 'Backend',  'name_v': 7, 'name_w': 10, 'desc': 'service',              'desc_v':  7},
            {'key': '7', 'name': 'Backend',  'name_v': 7, 'name_w': 10, 'desc': 'ingress - blue/green', 'desc_v': 20},
            {'key': '8', 'name': 'Backend',  'name_v': 7, 'name_w': 10, 'desc': 'ingress - canary',     'desc_v': 16},
            {'key': '9', 'name': '뒤로가기', 'name_v': 8},
        ])
        choice = _safe_input_number('\033[1;96m[ 메뉴를 선택하세요 ] ▶ \033[0m')
        if not choice:
            print("문자는 처리가 되지 않습니다.")
            continue
        if int(choice) == 9:
            return ''
        if int(choice) < 1 or int(choice) >= len(selection_list):
            continue
        return create_gitops_repository(selection_list[int(choice)], env_dict)

# =========================
# env 저장소 생성 (dev/stg/prod) — 경로 정규화 + self-signed 대응
# =========================
def create_registry(data):
    base = _api_base_from_host_url(data['gitea_host_url'])
    org  = f"{data['organization_name']}-cicd"
    auth = (data['git_cicd_id'], data['git_cicd_pw'])
    envs = ['dev', 'stg', 'prod']

    # 스킴별 verify 처리
    is_https = base.startswith('https://')
    verify_tls = bool(data.get('gitea_verify_tls', True)) if is_https else True
    if is_https and not verify_tls:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

    def _req(method, url, **kw):
        if is_https:
            kw.setdefault('verify', verify_tls)
        kw.setdefault('timeout', 15)
        return requests.request(method, url, auth=auth, **kw)

    # 목록 조회
    try:
        lr = _req('GET', f"{base}/orgs/{org}/repos")
        if lr.ok:
            existing = {r.get("name", "") for r in lr.json()}
        else:
            # HTTPS & 인증서 이슈가 의심되면 마지막으로 verify=False 재시도
            if is_https and verify_tls:
                lr = requests.get(f"{base}/orgs/{org}/repos", auth=auth, timeout=15, verify=False)
                existing = {r.get("name","") for r in (lr.json() if lr.ok else [])}
            else:
                existing = set()
        if not lr.ok:
            print(f"[create_registry] list fail: {lr.status_code} {lr.text[:200]}")
    except Exception as e:
        print(f"[create_registry] list exception: {e}")
        existing = set()

    # 생성
    for env in envs:
        repo_name = f"{data['application_name']}-{env}"
        if repo_name in existing:
            print(f"[create_registry] skip exists: {repo_name}")
            continue
        payload = {"name": repo_name, "private": True, "auto_init": True}
        try:
            r = _req('POST', f"{base}/orgs/{org}/repos", json=payload)
            if (not r.ok) and is_https and verify_tls:
                r = requests.post(f"{base}/orgs/{org}/repos", auth=auth, json=payload, timeout=15, verify=False)
            print(f"[create_registry] create {repo_name} -> {r.status_code} body={r.text[:200]}")
        except Exception as e:
            print(f"[create_registry] create EXCEPTION {repo_name}: {e}")
            continue

# =========================
# GitOps 생성: 템플릿 렌더/커밋/푸시
# =========================
def create_gitops_repository(env_param, env_param_dict):
    import shutil
    import subprocess as cmd

    # 0) init 로드
    result_path = f'./result/{env_param_dict["project_name"]}'
    init_file = f'{result_path}/{env_param_dict["project_name"]}-init_result.json'
    if not os.path.exists(init_file):
        return "초기화 파일이 존재하지 않습니다. 초기화 작업을 먼저 수행해주세요"
    with open(init_file, 'r') as f_in:
        data = json.load(f_in)

    data['organization_name'] = env_param_dict['organization_name']
    data['application_name']  = env_param_dict['application_name']

    gitops_folder = data["application_name"] + "-gitops"
    repo_root = os.path.join(os.getcwd(), gitops_folder)

    # 1) 조직/레포 생성
    create_organization(data)
    create_gitops(data)

    # 2) 기존 로컬 폴더 제거 후 클론
    if os.path.exists(gitops_folder):
        shutil.rmtree(gitops_folder)
    gitea_scheme = 'https' if data.get('gitea_domain', '').startswith('https://') else 'http'
    clone_url = (
        '{scheme}://{id}:{pw}@{host}/{org}-cicd/{app}-gitops.git'
        .format(scheme=gitea_scheme, id=_urlquote(data["git_cicd_id"], safe=''),
                pw=_urlquote(data["git_cicd_pw"], safe=''),
                host=data["gitea_host_url"],
                org=data["organization_name"], app=data["application_name"])
    )
    try:
        cmd.run(['git', '-c', 'http.sslVerify=false', 'clone', clone_url], check=True)
    except cmd.CalledProcessError as e:
        return f"git clone 실패 (종료코드 {e.returncode}): Gitea 접속·인증·레포 존재 여부를 확인하세요."

    # 3) 템플릿 루트 (실제 폴더명에 맞춰 하나만 두세요)
    TEMPLATE_ROOTS = ["./04.gitea-source"]
    template_root = next((p for p in TEMPLATE_ROOTS if os.path.isdir(p)), None)
    if not template_root:
        return "템플릿 디렉토리를 찾을 수 없습니다."

    env_key = (env_param or "").lower()

    # sample-<env_key>-gitops 탐색
    expected_top = os.path.join(template_root, f"sample-{env_key}-gitops")
    source_top = expected_top if os.path.isdir(expected_top) else None
    if source_top is None:
        for root, dirs, _ in os.walk(template_root):
            base = os.path.basename(root)
            if base.startswith("sample-") and base.endswith("-gitops") and env_key in base.lower():
                source_top = root
                break
    if source_top is None:
        return f"템플릿에서 최상단 폴더(sample-{env_key}-gitops)를 찾을 수 없습니다."

    # 4) 렌더/복사 — 로더를 template_root로, get_template는 로더 기준 상대경로
    from pathlib import Path
    j2 = Environment(loader=FileSystemLoader(template_root), autoescape=False)

    TEMPLATE_EXT = ('.yaml', '.yml', '.j2', '.tpl')  # 템플릿 확장자 모두 지원
    created_paths = []

    for root, _, files in os.walk(source_top):
        for fn in files:
            src_path = os.path.join(root, fn)
            rel_from_loader = os.path.relpath(src_path, start=template_root)  # 로더 기준
            rel_from_top    = os.path.relpath(src_path, start=source_top)
            rel_from_top    = rel_from_top.replace(f"sample-{env_key}", data["application_name"])

            # 산출물 확장자 정규화 (foo.yaml.j2 → foo.yaml)
            dest_rel = rel_from_top
            if fn.endswith('.yaml.j2') or fn.endswith('.yaml.tpl'):
                dest_rel = rel_from_top.rsplit('.', 1)[0]  # .j2/.tpl 제거
            elif fn.endswith('.yml.j2') or fn.endswith('.yml.tpl'):
                dest_rel = rel_from_top.rsplit('.', 1)[0]
            elif fn.endswith('.j2') or fn.endswith('.tpl'):
                dest_rel = rel_from_top.rsplit('.', 1)[0]

            dest_path = os.path.join(repo_root, dest_rel)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            if fn.endswith(TEMPLATE_EXT):
                # 템플릿 렌더
                template = j2.get_template(rel_from_loader)
                output   = template.render(data)
                with open(dest_path, 'w') as f_out:
                    f_out.write(output)
                created_paths.append(dest_path)
            else:
                # 비-템플릿 파일은 그대로 복사
                shutil.copy2(src_path, dest_path)
                created_paths.append(dest_path)

    # 디버그: 일부 경로 출력
    if created_paths:
        prefix = os.getcwd() + "/"
        show = [p.replace(prefix, "") for p in created_paths[:12]]
        print("[WRITE] sample outputs:\n" + "\n".join(show))
        print(f"[WRITE] total files written: {len(created_paths)}")
    else:
        print("[WRITE] 아무 파일도 생성되지 않았습니다. 템플릿 경로/확장자를 확인하세요.")

    # 5) env 저장소 생성(org-cicd)
    create_registry(data)
    print("[CHECK] expecting env repos:", [f"{data['application_name']}-{e}" for e in ['dev','stg','prod']])

    # 6) 커밋/푸시 — 변경/스테이징 확인
    original_cwd = os.getcwd()
    try:
        cmd.run(['git', 'config', '--global', '--add', 'safe.directory',
        os.path.join(original_cwd, gitops_folder)], check=True)
        os.chdir(gitops_folder)
        cmd.run(['git', 'config', 'http.sslVerify', 'false'], check=True)

        status = cmd.run(['git', 'status', '--porcelain'], check=True, capture_output=True, text=True).stdout.strip()
        print("[GIT] status:\n" + (status if status else "(empty)"))

        cmd.run(['git', 'add', '-A'], check=True)
        staged = cmd.run(['git', 'diff', '--cached', '--name-only'], check=True, capture_output=True, text=True).stdout.strip()
        print("[GIT] staged:\n" + (staged if staged else "(empty)"))

        if staged:
            cmd.run(['git', 'commit', '-m', 'gitops init'], check=True)
            cmd.run(['git', 'push'], check=True)
        else:
            print("스테이징된 파일이 없습니다. .gitignore/경로를 확인하세요.")
    except cmd.CalledProcessError as e:
        os.chdir(original_cwd)
        # e.cmd 전체 출력 금지 (clone URL 등 credential 노출 방지)
        cmd_summary = e.cmd[0] if isinstance(e.cmd, list) else str(e.cmd).split()[0]
        return f"git 작업 실패 ({cmd_summary} 종료코드 {e.returncode})"
    finally:
        os.chdir(original_cwd)

    # 7) 로컬 정리
    if os.path.exists(gitops_folder):
        shutil.rmtree(gitops_folder)

    input('\033[0m계속하려면 엔터를 눌러주세요. ')
    return "정상처리"

