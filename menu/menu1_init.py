import os
import sys
import json
import base64
try:
    import tomllib
except ImportError:
    import tomli as tomllib
from jinja2 import Environment, FileSystemLoader
import inquirer
import pexpect
import subprocess
from menu.util.component_api import *
from menu.util.ui import draw_menu, safe_prompt

# 필수 항목 및 기본값(플레이스홀더) 정의
_REQUIRED_FIELDS = [
    'project_name', 'nks_master_server', 'node_selector', 'nnd_cluster_name',
    'nnd_domain_name', 'gitea_domain', 'gitea_host_url',
    'image_registry',
    'nexus_domain',
]
# oauth_client_id/secret 은 OIDC 사용 시만 필요,
# vm_ssh_private/public_key 는 maven-spring-vm 파이프라인 사용 시만 필요 → 메뉴 진입 조건에서 제외
_PLACEHOLDERS = {
    '-----BEGIN CERTIFICATE-----\n-----END CERTIFICATE-----',
    '-----BEGIN PRIVATE KEY-----\n-----END PRIVATE KEY-----',
}

def validate_config(data: dict) -> bool:
    errors = [k for k in _REQUIRED_FIELDS if not data.get(k) or data.get(k) in _PLACEHOLDERS]
    if errors:
        print('\033[91m[CONFIG ERROR] 아래 필수 항목이 비어 있거나 기본값 상태입니다:\033[0m')
        for k in errors:
            print(f'\033[93m  - {k}\033[0m')
        print('\033[91m./00.reset/tekton_init.toml 을 먼저 작성해주세요.\033[0m')
        return False
    return True

_MENU1_NOTES = [
    '아래의 값들을 ./00.reset/tekton_init.toml 에 작성바랍니다.',
    '- node_selector        : ND 컴포넌트가 실행될 노드  ※ 여러 노드: "worker-0,worker-1"',
    '- cicd_cache_node_ip   : 캐시 노드 IP              ※ 여러 노드: "1.1.1.1,2.2.2.2"',
    '- nks_master_server    : nks 마스터서버 url',
    '- cicdbot_token        : 01.init 실행후 kubectl describe secret cicdbot token값을 반영',
    '- image_registry       : harbor 주소',
    '- harbor_robot_auth    : 로봇계정 생성시 발행된 값',
    '- oauth_client_id/secret : gitea에 등록된 OAuth2 앱 정보',
    '- wildcard_*_ssl_crt/key : 와일드카드 TLS 인증서 (개행은 \\n 으로 표기)',
    '- vm_ssh_private/public_key : VM SSH 배포용 키 (maven-spring-vm 사용시)',
]

def menu1():
    """
    Tekton 초기화 전체 흐름 메뉴.
    1. 환경 파일 로딩
    2. 인증정보 base64 인코딩(필요시)
    3. 반복적으로 메뉴 출력 및 입력 분기
    """
    # --- 환경 파일 로드 및 인증정보 추가 ---
    with open('./00.reset/tekton_init.toml', 'rb') as f_in:
        data = tomllib.load(f_in)
    if not validate_config(data):
        input('\033[0m계속하려면 엔터를 눌러주세요. ')
        return
    result_path = './result/' + data['project_name']
    os.makedirs(result_path, exist_ok=True)

    def add_b64(key_id, key_pw, key_result):
        if key_id in data and key_pw in data:
            v = f"{data[key_id]}:{data[key_pw]}"
            data[key_result] = base64.b64encode(v.encode('utf-8')).decode('utf-8')
    add_b64('harbor_id', 'harbor_pw', 'harbor_auth')
    # add_b64('harbor_robot_id', 'harbor_robot_pw', 'harbor_robot_auth')
    add_b64('harbor_admin_id', 'harbor_admin_pw', 'harbor_admin_auth')
    add_b64('git_cicd_id', 'git_cicd_pw', 'git_cicd_auth')
    data['node_selector_list'] = [n.strip() for n in str(data.get('node_selector', '')).split(',') if n.strip()]

    # --- 메뉴 반복 ---
    while True:
        draw_menu('1.  초기화', 10, [
            {'key': '1', 'name': 'tekton_init.toml 값 확인', 'name_v': 24},
            {'key': '2', 'name': '초기화 실행',               'name_v': 11},
            {'key': '3', 'name': 'ArgoCD 비밀번호 설정',       'name_v': 20},
            {'key': '9', 'name': '뒤로가기',                   'name_v':  8},
        ], notes=_MENU1_NOTES)

        munu_number = input('\033[1;96m[ 메뉴를 선택하세요 ] ▶ \033[0m').strip()

        if not munu_number.isnumeric():
            print('\033[31m' + '문자는 처리가 되지 않습니다.' + '\033[0m')
            continue

        sel = int(munu_number)
        if sel == 1:
            screen_init_value(data)
        elif sel == 2:
            tekton_init_execute(result_path, data)
        elif sel == 3:
            print('\033[31m' + "ArgoCD ConfigMap이 등록이 되어 있어야 실행이 가능합니다. 아래 명령어로 계정여부를 확인바랍니다." + '\033[0m')
            print('\033[33m' + "kubectl get cm argocd-cm -n argocd -o yaml" + '\033[0m')
            print('\033[31m' + "하위 패스의 경우 아래의 옵션도 추가 되어야 합니다." + '\033[0m')
            print('\033[33m' + "--grpc-web-root-path argocd" + '\033[0m')
            options = [inquirer.List("option", message="계속 진행하시겠습니까?", choices=['예', '아니오'])]
            select = safe_prompt(options)
            if select and select['option'] == '예':
                argocd_password_init(data)
        elif sel == 9:
            return
        else:
            print('\033[31m' + '메뉴내의 숫자만 입력가능합니다. 입력된값 : ' + munu_number + '\033[0m')
            continue

def argocd_password_init(data):
    """
    ArgoCD 계정 비밀번호 자동 변경. (pexpect로 자동 입력)
    """
    init_component_id = [k for k in data if 'component_account_id' in k]
    subprocess.run(
        ['./argocd-linux-amd64', 'login', data['argocd_host_url'],
         '--skip-test-tls', '--grpc-web', '--insecure',
         '--username', data['argocd_admin_id'],
         '--password', data['argocd_admin_pw']],
        capture_output=True, text=True
    )
    try:
        for item in init_component_id:
            process = pexpect.spawn(
                './argocd-linux-amd64',
                args=['account', 'update-password', '--account', data[item]],
                encoding="utf-8", timeout=10, logfile=sys.stdout
            )
            process.sendline(data['argocd_admin_pw'])
            pw = data[item.replace('id', 'pw')]
            process.sendline(pw)
            process.sendline(pw)
            process.expect(pexpect.EOF)
            print("Password updated successfully.")
    except pexpect.exceptions.TIMEOUT as e:
        print("Timeout occurred:", e)
    except Exception as e:
        print("An error occurred:", e)

def screen_init_value(init_data):
    """
    환경값을 20개씩 끊어서 보여주고, 계속은 아무 키 입력.
    """
    print_size = 20
    wait_point = 0
    for k, v in init_data.items():
        print('\033[95m' + k + ': ' + '\033[37m' + str(v) + '\033[0m')
        wait_point += 1
        if wait_point == print_size:
            input('\033[0m계속하려면 엔터를 눌러주세요. ')
            wait_point = 0

def init_yaml_create(result_path, init_data):
    """
    01.init 하위 모든 yaml 템플릿을 읽어서 result에 렌더링 출력
    - tekton-catalog 관련 여부로 파일 분리 저장
    - oauth 파일은 별도 저장
    """
    yaml_list = []
    menu1_file = result_path + '/01-2.init-pipeline.yaml'
    menu1_2_file = result_path + '/01-1.init-basic.yaml'
    menu1_3_file = result_path + '/01-3.init-oauth.yaml'
    menu1_4_file = result_path + '/01-4.init-argo.yaml'
    menu1_5_file = result_path + '/01-5.init-tekton-group-role.yaml'
    menu1_6_file = result_path + '/01-6.init-cluster.yaml'

    # 결과 파일 초기화
    for f in [menu1_file, menu1_2_file, menu1_3_file, menu1_4_file, menu1_5_file, menu1_6_file]:
        with open(f, 'w'):
            pass

    project_file = open(menu1_file, 'a')
    project1_2_file = open(menu1_2_file, 'a')
    project1_3_file = open(menu1_3_file, 'a')
    project1_4_file = open(menu1_4_file, 'a')
    project1_5_file = open(menu1_5_file, 'a')
    project1_6_file = open(menu1_6_file, 'a')
    try:
        # 파이프라인 파일 헤더
        project_file.write("apiVersion: v1\n")
        project_file.write("kind: Namespace\n")
        project_file.write("metadata:\n")
        project_file.write("  name: tekton-catalog\n")

        # 템플릿 수집
        for (path, dir, files) in os.walk("./01.init"):
            for filename in files:
                ext = os.path.splitext(filename)[-1]
                if ext == '.yaml':
                    yaml_list.append(path + "/" + filename)

        file_loader = FileSystemLoader('./')
        env = Environment(loader=file_loader)
        for item in yaml_list:
            template = env.get_template(item)
            output = template.render(init_data)
            item_path = item.replace("\\", "/")
            if "/oauth/" in item_path:
                project1_3_file.write("\n---\n")
                project1_3_file.write(output)
            elif "/tekton-catalog/" in item_path:
                project_file.write("\n---\n")
                project_file.write(output)
            elif "/tekton-with-role/" in item_path:
                project1_2_file.write("\n---\n")
                project1_2_file.write(output)
            elif "/argocd/" in item_path:
                project1_4_file.write("\n---\n")
                project1_4_file.write(output)
            elif "/tekton-group-role/" in item_path:
                project1_5_file.write("\n---\n")
                project1_5_file.write(output)
            elif item_path.split('/')[-2] == '01.init':
                # 01.init 루트의 *cluster.yaml — 어플리케이션 클러스터 초기 설정
                project1_6_file.write("\n---\n")
                project1_6_file.write(output)
            else:
                print(f"[WARN] {item} 분기 없음, 건너뜁니다.")
    finally:
        project_file.close()
        project1_2_file.close()
        project1_3_file.close()
        project1_4_file.close()
        project1_5_file.close()
        project1_6_file.close()

def tekton_init_execute(result_path, init_data):
    """
    Tekton 등 기본 infra 리소스, 계정, 저장소 초기화 자동화
    - yaml 템플릿 생성
    - harbor, nexus 등 연동 리소스 및 토큰 자동생성
    """
    print('\033[31m' + "이미지 저장소로 harbor을 사용합니까?" + '\033[0m')
    options = [inquirer.List("option", message="계속 진행하시겠습니까?", choices=['예','아니오'])]
    select = safe_prompt(options)

    init_yaml_create(result_path, init_data)

    if select and select['option'] == '예':
        create_harbor_robot_id(init_data)

    init_component_id = [k for k in init_data if 'component_account_id' in k]
    temp_init = init_data.copy()
    for item in init_component_id:
        pw = init_data[item.replace('id', 'pw')]
        temp_init['harbor_id'] = temp_init['git_cicd_id'] = temp_init['nexus_id'] = init_data[item]
        temp_init['harbor_pw'] = temp_init['git_cicd_pw'] = temp_init['nexus_pw'] = pw
        create_gitea_user_id(temp_init)
        create_nexus_id(temp_init)
        if select and select['option'] == '예':
            create_harbor_id(temp_init)

    # 저장소 및 소나큐브 등 기타 연동 리소스 자동생성
    create_nexus_maven_repository(init_data)
    create_nexus_maven_group_repository(init_data)
    create_nexus_npm_repository(init_data)
    create_nexus_npm_group_repository(init_data)
    create_nexus_raw_repository(init_data)
    create_nexus_raw_group_repository(init_data)
    create_sonar_token(init_data)

    with open(os.path.join(result_path, f"{init_data['project_name']}-init_result.json"), "w") as json_file:
        json.dump(init_data, json_file)

    print('\033[31m초기화된 값을 확인후 파일을 실행해 주세요.\033[0m')
    print('\033[31mtekton의 rbac가 적용된 경우 nginx-ingress의 sniffit을 수정해주세요\033[0m')
    print('\033[31mtekton의 rbac가 적용된 경우 내부망은 coredns의 host를 gitea를 찾아갈 수 있게 설정해야합니다.\033[0m')
    print('\033[31mpem키를 복사해서 result폴더에 넣어주세요\033[0m')
    print('\033[33msed -i "s/cicdbot_secret_token/$(kubectl describe secret cicdbot -n default | grep token: | awk \'{{ print $2 }}\')/g" "./result/{}/{}-init_result.json"\033[0m'
           .format(init_data['project_name'], init_data['project_name']))
    input('\033[0m계속하려면 엔터를 눌러주세요. ')

