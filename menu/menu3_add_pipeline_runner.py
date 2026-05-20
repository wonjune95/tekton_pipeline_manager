import os
import json
import base64
import subprocess
import requests
import inquirer
import re
from jinja2 import Environment, FileSystemLoader
from menu.util.component_api import *
from menu.util import component_api as _cap
from menu.util.ui import draw_menu, safe_prompt, validate_k8s_name

def _pick(*names):
    for n in names:
        if hasattr(_cap, n):
            return getattr(_cap, n)
    return None

get_organization  = _pick("get_organization", "get_oragnizaion", "get_organizations")
get_repos_in_orgs = _pick("get_repos_in_orgs", "get_repos_in_org", "list_repos_in_org")

# ======================================
# Tekton 파이프라인 러너 생성 메인 메뉴
# ======================================
def menu3():
    return_string = ''
    while True:
        draw_menu('3.  파이프라인', 14, [
            {'key': '1', 'name': '설정값 확인',   'name_v': 11},
            {'key': '2', 'name': '자동선택 모드', 'name_v': 13},
            {'key': '3', 'name': '수동입력 모드', 'name_v': 13},
            {'key': '9', 'name': '뒤로가기',      'name_v':  8},
        ], notes=[
            '자동선택모드는 Gitea와 연동이 되어야 실행 가능합니다.',
            '수동입력모드는 조직명과 어플리케이션명을 직접 입력해야합니다.',
        ])
        if return_string:
            color = '\033[92m' if return_string == '정상처리' else '\033[91m'
            print(f"{color}{return_string}\033[0m")
        menu_number = input('\033[1;96m[ 메뉴를 선택하세요 ] ▶ \033[0m').strip()
        if not menu_number.isdigit():
            print('\033[31m문자는 처리가 되지 않습니다.\033[0m')
            continue
        sel = int(menu_number)
        if sel == 1:
            screen_init_value()
        elif sel == 2:
            return_string = add_pipeline_runner_execute()
        elif sel == 3:
            return_string = manual_mode()
        elif sel == 9:
            return
        else:
            print(f'\033[31m메뉴내의 숫자만 입력가능합니다. 입력된값 : {menu_number}\033[0m')
            continue

# =========================
# 프로젝트 선택(폴더 리스트)
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
        options = [inquirer.List("option", message="프로젝트를 선택해주세요", choices=project_list)]
        select = safe_prompt(options)
        if not select:
            return None
        return select['option']
    return project_list[0]

# =========================
# 환경 값 확인
# =========================
def screen_init_value():
    project_name = choice_project()
    if project_name is None:
        return
    result_path = f'./result/{project_name}'
    result_file = f'{result_path}/{project_name}-init_result.json'
    if not os.path.exists(result_file):
        print('\033[91m초기화 파일이 존재하지 않습니다. 초기화 작업을 먼저 수행해주세요\033[0m')
        return
    with open(result_file, 'r') as f_in:
        data = json.load(f_in)
    print('\033[96mproject_name: \033[37m' + data['project_name'] + '\033[0m')
    input('\033[0m계속하려면 엔터를 눌러주세요. ')

# =========================
# 자동선택 모드(조직/앱 선택)
# =========================
def add_pipeline_runner_execute():
    env_dict = {}
    project_name = choice_project()
    if project_name is None:
        return ''
    env_dict['project_name'] = project_name
    result_path = f'./result/{project_name}'
    init_file = f'{result_path}/{project_name}-init_result.json'
    if not os.path.exists(init_file):
        return "초기화 파일이 존재하지 않습니다. 초기화 작업을 먼저 수행해주세요"
    with open(init_file, 'r') as f_in:
        data = json.load(f_in)
    env_dict['gitea_domain'] = data['gitea_domain']
    env_dict['git_cicd_auth'] = data['git_cicd_auth']
    try:
        org_res = json.loads(get_organization(env_dict))
    except (requests.HTTPError, requests.ConnectionError, ValueError) as e:
        return f"Gitea API 오류 (조직 조회 실패): {e}"
    organization_name_list = [item['name'] for item in org_res if 'cicd' not in item['name']]
    if not organization_name_list:
        return "조직이 존재하지 않습니다. 조직생성후 재실행하시길 바랍니다."
    options = [inquirer.List("option", message="조직명을 선택해주세요", choices=organization_name_list)]
    select = safe_prompt(options)
    if not select:
        return ''
    env_dict['organization_name'] = select['option']
    try:
        app_res = json.loads(get_repos_in_orgs(env_dict))
    except (requests.HTTPError, requests.ConnectionError, ValueError) as e:
        return f"Gitea API 오류 (레포 조회 실패): {e}"
    application_name_list = [item['name'] for item in app_res]
    if not application_name_list:
        return "어플리케이션이 존재하지 않습니다. 어플리케이션생성후 재실행하시길 바랍니다."
    options = [inquirer.List("option", message="어플리케이션을 선택해주세요", choices=application_name_list)]
    select = safe_prompt(options)
    if not select:
        return ''
    env_dict['application_name'] = select['option']
    return choice_pipeline(env_dict)

# =========================
# 수동입력 모드(직접 조직/앱명 입력)
# =========================
def manual_mode():
    env_dict = {}
    project_name = choice_project()
    if project_name is None:
        return ''
    env_dict['project_name'] = project_name
    org_name = input('\033[96m조직명을 입력해주세요(소문자·숫자·하이픈, 예시: sample): \033[0m').strip()
    err = validate_k8s_name(org_name, '조직명')
    if err:
        return err
    env_dict['organization_name'] = org_name
    app_name = input('\033[96m어플리케이션명을 입력해주세요(소문자·숫자·하이픈, 예시: product-frontend): \033[0m').strip()
    err = validate_k8s_name(app_name, '어플리케이션명')
    if err:
        return err
    env_dict['application_name'] = app_name
    return choice_pipeline(env_dict)

# =========================
# 파이프라인 유형 및 환경/브랜치/클러스터 선택
# =========================
def choice_pipeline(env_dict):
    selection_list = ['','npm-argo','maven-boot-argo','maven-tomcat-argo','maven-spring-vm','gradle-boot-argo','gradle-tomcat-argo','spring-library']
    result_path = f'./result/{env_dict["project_name"]}'
    env_dict['result_path'] = result_path
    init_file = f'{result_path}/{env_dict["project_name"]}-init_result.json'
    if not os.path.exists(init_file):
        return "초기화 파일이 존재하지 않습니다. 초기화 작업을 먼저 수행해주세요"
    with open(init_file, 'r') as f_in:
        data = json.load(f_in)
    while True:
        draw_menu('파이프라인 유형 선택', 20, [
            {'key': '1', 'name': 'Frontend', 'name_v': 8, 'name_w': 10, 'desc': 'build(npm-nginx) + deploy(argocd)',            'desc_v': 33},
            {'key': '2', 'name': 'Backend',  'name_v': 7, 'name_w': 10, 'desc': 'build(maven-boot) + deploy(argocd)',           'desc_v': 34},
            {'key': '3', 'name': 'Backend',  'name_v': 7, 'name_w': 10, 'desc': 'build(maven-spring+tomcat) + deploy(argocd)', 'desc_v': 43},
            {'key': '4', 'name': 'Backend',  'name_v': 7, 'name_w': 10, 'desc': 'build(maven-spring) + deploy(vm-ssh)',         'desc_v': 36},
            {'key': '5', 'name': 'Backend',  'name_v': 7, 'name_w': 10, 'desc': 'build(gradle-boot) + deploy(argocd)',          'desc_v': 35},
            {'key': '6', 'name': 'Backend',  'name_v': 7, 'name_w': 10, 'desc': 'build(gradle-spring+tomcat) + deploy(argocd)','desc_v': 44},
            {'key': '7', 'name': 'Library',  'name_v': 7, 'name_w': 10, 'desc': 'build(maven-spring-library)',                  'desc_v': 27},
            {'key': '9', 'name': '뒤로가기', 'name_v': 8},
        ])
        choice = input('\033[1;96m[ 메뉴를 선택하세요 ] ▶ \033[0m').strip()
        if not choice.isdigit():
            return "문자는 처리가 되지 않습니다."
        if int(choice) == 9:
            return ''
        if int(choice) < 1 or int(choice) >= len(selection_list):
            print(f'\033[31m1~{len(selection_list)-1} 사이의 번호를 입력하세요.\033[0m')
            continue
        envVal = input('\033[96m생성할 환경명을 입력해주세요(소문자·숫자·하이픈, 예시: dev, stg, prod): \033[0m').strip()
        err = validate_k8s_name(envVal, '환경명')
        if err:
            return err
        env_dict['env_menu'] = envVal
        branchVal = input('\033[96m생성된 브랜치명을 입력해주세요(예시: dev, main): \033[0m').strip()
        if not branchVal:
            return '브랜치명을 입력해주세요.'
        env_dict['branch_menu'] = branchVal
        if selection_list[int(choice)] not in ('maven-spring-vm', 'spring-library'):
            deploy_cluster = [k for k in data if k.endswith('deploy_cluster')]
            options = [inquirer.List("option", message="배포될 클러스터를 선택해 주세요", choices=deploy_cluster)]
            select = safe_prompt(options)
            if not select:
                return ''
            env_dict['deploy_cluster'] = data[select['option']]
        return generate_pipeline_run_yaml(selection_list[int(choice)], env_dict, data)

# =========================
# 실제 파이프라인 yaml 파일 생성/저장
# =========================
def generate_pipeline_run_yaml(pipeline_param, env_param_dict, init_data):
    # 파라미터/템플릿값 조합
    temp_data = init_data.copy()
    temp_data['env_menu'] = env_param_dict['env_menu']
    temp_data['branch_menu'] = env_param_dict['branch_menu']
    if 'deploy_cluster' in env_param_dict:
        temp_data['deploy_cluster'] = env_param_dict['deploy_cluster']
    temp_data['organization_name'] = env_param_dict['organization_name']
    temp_data['application_name'] = env_param_dict['application_name']
    result_path = os.path.join(
        env_param_dict['result_path'],
        f"{env_param_dict['organization_name']}-cicd",
        env_param_dict['application_name']
    )
    os.makedirs(result_path, exist_ok=True)
    menu3_file = os.path.join(
        result_path,
        f"03.add-app-in-organization-{env_param_dict['application_name']}-{temp_data['env_menu']}.yaml"
    )
    if os.path.exists(menu3_file):
        os.remove(menu3_file)
    yaml_list = []
    for path, dir, files in os.walk("./03.add-app-in-organization"):
        for filename in files:
            if pipeline_param in path and filename.endswith('.yaml'):
                yaml_list.append(os.path.join(path, filename))
    file_loader = FileSystemLoader('./')
    env = Environment(loader=file_loader)
    with open(menu3_file, 'a') as project_file:
        for item in yaml_list:
            project_file.write("\n---\n")
            template = env.get_template(item)
            output = template.render(temp_data)
            project_file.write(output)
    options = [inquirer.List("option", message="파일을 자동적용 하시겠습니까?", choices=['Yes', 'No'])]
    select = safe_prompt(options)
    if select and select['option'] == 'Yes':
        try:
            subprocess.run(['kubectl', 'config', 'use-context', temp_data['nnd_cluster_name']], check=True)
            result = subprocess.run(['kubectl', 'apply', '-f', menu3_file], capture_output=True, text=True)
            print(result.stdout)
            if result.returncode != 0:
                print('\033[91m' + result.stderr + '\033[0m')
                return f"kubectl apply 실패 — 생성된 파일을 직접 확인하세요: {menu3_file}"
        except subprocess.CalledProcessError as e:
            print(f'\033[91mkubectl 실행 실패 (종료코드 {e.returncode}): {e.cmd}\033[0m')
            return f"kubectl 실패 — 생성된 파일을 직접 확인하세요: {menu3_file}"
    return "정상처리"
