import os
import re
import json
import base64
import subprocess
import inquirer
import paramiko
from jinja2 import Environment, FileSystemLoader
from menu.util.ui import draw_menu, safe_prompt, validate_k8s_name

def _load_private_key(pem_path):
    for key_cls in (paramiko.RSAKey, paramiko.ECDSAKey, paramiko.Ed25519Key, paramiko.DSSKey):
        try:
            return key_cls.from_private_key_file(pem_path)
        except paramiko.SSHException:
            continue
    raise ValueError(f"지원하지 않는 키 형식: {pem_path}")

# =========================
# Tekton 조직추가 메인 메뉴
# =========================
def menu2():
    while True:
        draw_menu('2.  조직 추가', 13, [
            {'key': '1', 'name': '설정값 확인',        'name_v': 11},
            {'key': '2', 'name': '조직추가 실행',      'name_v': 13},
            {'key': '3', 'name': '캐시 폴더 초기화',   'name_v': 15},
            {'key': '9', 'name': '뒤로가기',           'name_v':  8},
        ], notes=[
            'rbac 파일은 필수요소입니다:',
            '  kubectl get ClusterRoleBinding cicdbot -o yaml > ./02-2.add-organization/rbac.yaml',
            '네이버와 NHN의 환경이 다르므로 RBAC의 내용을 확인하시고 적용바랍니다.',
            '02-1.add-storage-in-organization 파일은 각 어플리케이션 클러스터에서 나눠서 실행하세요!!!',
            'ND 클러스터 cache 노드에 /CICD-DATA/local/{org}-cicd, /CICD-DATA/store/{org}-cicd 폴더를 생성하세요!!!',
        ])
        menu_number = input('\033[1;96m[ 메뉴를 선택하세요 ] ▶ \033[0m').strip()
        if not menu_number.isdigit():
            print('\033[31m문자는 처리가 되지 않습니다.\033[0m')
            continue
        sel = int(menu_number)
        if sel == 1:
            screen_init_value()
        elif sel == 2:
            add_org_execute()
        elif sel == 3:
            reset_cache_folders()
        elif sel == 9:
            return
        else:
            print('\033[31m메뉴내의 숫자만 입력가능합니다. 입력된값 : ' + menu_number + '\033[0m')
            continue

# =========================
# 프로젝트 선택(폴더 리스트 기반)
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
    options = [inquirer.List("option", message="조직을 추가할 프로젝트를 선택해주세요", choices=project_list)]
    select = safe_prompt(options)
    if not select:
        return None
    return select['option']

# =========================
# 환경 값(노드 정보) 확인 화면
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
    print('\033[96mcicd_cache_node_ip: \033[37m' + data.get('cicd_cache_node_ip', '') + '\033[0m')
    print('\033[96mcicd_cache_node_id: \033[37m' + data.get('cicd_cache_node_id', '') + '\033[0m')
    input('\033[0m계속하려면 엔터를 눌러주세요. ')

# =========================
# 조직추가 실행(템플릿 렌더링/적용)
# =========================
def add_org_execute():
    job_folder_list = []
    pem_exist_at = False
    pem_path = None

    project_name = choice_project()
    if project_name is None:
        return
    result_path = f'./result/{project_name}'
    result_file = f'{result_path}/{project_name}-init_result.json'

    file_list = os.listdir(result_path)
    for item in file_list:
        if item.endswith('.pem'):
            pem_exist_at = True
            pem_path = os.path.join(result_path, item)

    if not os.path.exists(result_file):
        print('\033[91m초기화 파일이 존재하지 않습니다. 초기화 작업을 먼저 수행해주세요\033[0m')
        input('\033[0m계속하려면 엔터를 눌러주세요. ')
        return

    if not os.path.exists('./02-2.add-organization/rbac.yaml'):
        print('\033[91mrbac.yaml이 존재하지 않습니다. 아래의 명령어로 rbac.yaml을 생성하세요\033[0m')
        print('\033[33mkubectl get ClusterRoleBinding cicdbot -o yaml > ./02-2.add-organization/rbac.yaml\033[0m')
        input('\033[0m계속하려면 엔터를 눌러주세요. ')
        return

    with open(result_file, 'r') as f_in:
        data = json.load(f_in)

    # 조직명 입력 및 경로 준비
    organization_name = input('\033[96m추가할 조직명을 입력해주세요(소문자·숫자·하이픈, 예: my-org): \033[0m').strip()
    err = validate_k8s_name(organization_name, '조직명')
    if err:
        print(f'\033[91m{err}\033[0m')
        return
    data['organization_name'] = organization_name
    org_result_path = os.path.join(result_path, f'{organization_name}-cicd')
    os.makedirs(org_result_path, exist_ok=True)

    # 02- 디렉토리 목록 추출
    job_folder_list = [f for f in ['02-1.add-storage-in-organization', '02-2.add-organization']
                       if os.path.isdir(f'./{f}')]
    file_apply_list = []

    # 폴더별 yaml 파일 처리
    for folder in job_folder_list:
        yaml_list = []
        for path, dir, files in os.walk(f"./{folder}"):
            for filename in files:
                if filename.endswith('.yaml'):
                    yaml_list.append(os.path.join(path, filename))
        file_loader = FileSystemLoader('./')
        env = Environment(loader=file_loader)
        if folder == "02-1.add-storage-in-organization":
            for item in yaml_list:
                file_path = f'{org_result_path}/02-1.{os.path.basename(item)}'
                file_apply_list.append(file_path)
                with open(file_path, 'w') as project_file:
                    template = env.get_template(item)
                    output = template.render(data)
                    project_file.write(output)
        else:
            yaml_list.sort(reverse=True)
            file_path = f'{org_result_path}/{folder}.yaml'
            file_apply_list.append(file_path)
            with open(file_path, 'w') as project_file:
                for idx, item in enumerate(yaml_list):
                    if idx == 0:
                        project_file.write("\n---\napiVersion: v1\nkind: Namespace\nmetadata:\n")
                        project_file.write(f"  name: {data['organization_name']}-cicd\n---\n")
                    if "rbac" in item:
                        with open(item) as f:
                            content = f.read()
                        kubectl_fields = ('annotations', 'creationTimestamp', 'resourceVersion',
                                          'uid', 'generation', 'managedFields', 'labels', 'selfLink')
                        for field in kubectl_fields:
                            content = re.sub(rf'\n  {field}:[ \S]*(\n    [^\n]*)*', '', content)
                        content = re.sub(r'\nsubjects:.*', '', content, flags=re.DOTALL)
                        content = content.rstrip() + (
                            f"\nsubjects:\n"
                            f"- kind: ServiceAccount\n"
                            f"  name: cicdbot\n"
                            f"  namespace: {data['organization_name']}-cicd\n"
                        )
                        project_file.write("\n---\n")
                        project_file.write(content)
                    else:
                        project_file.write("\n---\n")
                        template = env.get_template(item)
                        output = template.render(data)
                        project_file.write(output)

    print('\033[91m네이버와 NHN의 환경이 다르므로 RBAC의 내용을 확인하시고 적용바랍니다\033[0m')
    print('\033[91m사용 완료된 ./02-2.add-organization/rbac.yaml 파일은 직접 삭제하세요\033[0m')
    print('\033[91m02-1.add-storage-in-organization 파일은 각 어플리케이션 클러스터에서 나눠서 실행하세요!!!\033[0m')

    # ND 클러스터 cache 노드 폴더 자동 생성(SSH) or 안내
    if pem_exist_at:
        key = _load_private_key(pem_path)
        node_ips = [ip.strip() for ip in data['cicd_cache_node_ip'].split(',') if ip.strip()]
        node_port = int(data.get('cicd_cache_node_port', 22))
        for ip in node_ips:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip, port=node_port, username=data['cicd_cache_node_id'], pkey=key)
            _, stdout, stderr = client.exec_command(f'sudo mkdir -p /CICD-DATA/local/{data["organization_name"]}-cicd /CICD-DATA/store/{data["organization_name"]}-cicd')
            stdout.channel.recv_exit_status()
            client.close()
            print(f'\033[96m[{ip}] 폴더 생성 완료\033[0m')
    else:
        print('\033[91mND 클러스터 cache가 되는 노드에 /CICD-DATA/local/{{organization_name}}-cicd, /CICD-DATA/store/{{organization_name}}-cicd 폴더를 생성하세요!!!\033[0m')

    # 자동 적용 여부 선택 및 명령어 안내
    options = [inquirer.List("option", message="파일을 자동적용 하시겠습니까?", choices=['Yes', 'No'])]
    select = safe_prompt(options)

    if select and select['option'] == 'Yes':
        try:
            dev_cluster = [k for k in file_apply_list if '02-1.dev' in k]
            for item in dev_cluster:
                context = item.split(".")[-2]
                subprocess.run(['kubectl', 'config', 'use-context', context], check=True)
                subprocess.run(['kubectl', 'apply', '-f', item], check=True)

            # stg/prod 는 각 클러스터에서 직접 실행 필요
            # for item in [k for k in file_apply_list if '02-1.stg' in k]:
            #     subprocess.run(['kubectl', 'config', 'use-context', item.split(".")[-2]], check=True)
            #     subprocess.run(['kubectl', 'apply', '-f', item], check=True)

            nnd_cluster = [k for k in file_apply_list if '02-2.add-organization.yaml' in k]
            for item in nnd_cluster:
                subprocess.run(['kubectl', 'config', 'use-context', data['nnd_cluster_name']], check=True)
                subprocess.run(['kubectl', 'apply', '-f', item], check=True)
        except subprocess.CalledProcessError as e:
            print(f'\033[91mkubectl 실행 실패 (종료코드 {e.returncode}): {e.cmd}\033[0m')
            print('\033[91m위 파일을 직접 확인 후 수동으로 적용하세요.\033[0m')
            input('\033[0m계속하려면 엔터를 눌러주세요. ')

# =========================
# 캐시 폴더 초기화 (삭제 후 재생성)
# =========================
def reset_cache_folders():
    project_name = choice_project()
    if project_name is None:
        return
    result_path = f'./result/{project_name}'
    result_file = f'{result_path}/{project_name}-init_result.json'

    if not os.path.exists(result_file):
        print('\033[91m초기화 파일이 존재하지 않습니다. 초기화 작업을 먼저 수행해주세요\033[0m')
        input('\033[0m계속하려면 엔터를 눌러주세요. ')
        return

    with open(result_file, 'r') as f_in:
        data = json.load(f_in)

    organization_name = input('\033[96m캐시를 초기화할 조직명을 입력해주세요: \033[0m').strip()
    if not organization_name:
        print('\033[91m조직명을 입력해주세요\033[0m')
        return

    print(f'\033[91m경고: /CICD-DATA/local/{organization_name}-cicd, /CICD-DATA/store/{organization_name}-cicd 폴더를 삭제 후 재생성합니다.\033[0m')
    confirm = input('\033[96m계속하시겠습니까? (yes 입력 시 진행): \033[0m').strip()
    if confirm != 'yes':
        print('취소되었습니다.')
        return

    pem_exist_at = False
    pem_path = None
    for item in os.listdir(result_path):
        if item.endswith('.pem'):
            pem_exist_at = True
            pem_path = os.path.join(result_path, item)

    if not pem_exist_at:
        print('\033[91m.pem 파일이 없습니다. 아래 명령어를 각 노드에서 직접 실행하세요\033[0m')
        print(f'\033[33msudo rm -rf /CICD-DATA/local/{organization_name}-cicd /CICD-DATA/store/{organization_name}-cicd\033[0m')
        print(f'\033[33msudo mkdir -p /CICD-DATA/local/{organization_name}-cicd /CICD-DATA/store/{organization_name}-cicd\033[0m')
        return

    key = _load_private_key(pem_path)
    node_ips = [ip.strip() for ip in data['cicd_cache_node_ip'].split(',') if ip.strip()]
    node_port = int(data.get('cicd_cache_node_port', 22))
    for ip in node_ips:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, port=node_port, username=data['cicd_cache_node_id'], pkey=key)
        _, stdout, _ = client.exec_command(
            f'sudo rm -rf /CICD-DATA/local/{organization_name}-cicd /CICD-DATA/store/{organization_name}-cicd'
            f' && sudo mkdir -p /CICD-DATA/local/{organization_name}-cicd /CICD-DATA/store/{organization_name}-cicd'
        )
        stdout.channel.recv_exit_status()
        client.close()
        print(f'\033[96m[{ip}] 캐시 폴더 초기화 완료\033[0m')
