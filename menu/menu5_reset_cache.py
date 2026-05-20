import os
import json
import inquirer
import paramiko
from menu.util.ui import safe_prompt, validate_k8s_name


def _load_private_key(pem_path):
    for key_cls in (paramiko.RSAKey, paramiko.ECDSAKey, paramiko.Ed25519Key, paramiko.DSSKey):
        try:
            return key_cls.from_private_key_file(pem_path)
        except paramiko.SSHException:
            continue
    raise ValueError(f"지원하지 않는 키 형식: {pem_path}")


def _choice_project():
    if not os.path.isdir('result'):
        print('\033[91m초기화된 프로젝트가 없습니다. 메뉴 1에서 초기화를 먼저 실행하세요.\033[0m')
        input('\033[0m계속하려면 엔터를 눌러주세요. ')
        return None
    project_list = [d for d in os.listdir('result') if os.path.isdir(os.path.join('result', d))]
    if not project_list:
        print('\033[91m초기화된 프로젝트가 없습니다. 메뉴 1에서 초기화를 먼저 실행하세요.\033[0m')
        input('\033[0m계속하려면 엔터를 눌러주세요. ')
        return None
    options = [inquirer.List("option", message="프로젝트를 선택해주세요", choices=project_list)]
    select = safe_prompt(options)
    if not select:
        return None
    return select['option']


def menu5():
    project_name = _choice_project()
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
    err = validate_k8s_name(organization_name, '조직명')
    if err:
        print(f'\033[91m{err}\033[0m')
        input('\033[0m계속하려면 엔터를 눌러주세요. ')
        return

    print(f'\033[91m경고: /CICD-DATA/local/{organization_name}-cicd, /CICD-DATA/store/{organization_name}-cicd 폴더를 삭제 후 재생성합니다.\033[0m')
    confirm = input('\033[96m계속하시겠습니까? (yes 입력 시 진행): \033[0m').strip()
    if confirm != 'yes':
        print('취소되었습니다.')
        return

    pem_path = None
    for search_dir in [result_path, 'result']:
        for item in os.listdir(search_dir):
            if item.endswith('.pem'):
                pem_path = os.path.join(search_dir, item)
                break
        if pem_path:
            break

    if not pem_path:
        print('\033[91m.pem 파일이 없습니다. 아래 명령어를 각 노드에서 직접 실행하세요\033[0m')
        print(f'\033[33msudo rm -rf /CICD-DATA/local/{organization_name}-cicd /CICD-DATA/store/{organization_name}-cicd\033[0m')
        print(f'\033[33msudo mkdir -p /CICD-DATA/local/{organization_name}-cicd /CICD-DATA/store/{organization_name}-cicd\033[0m')
        return

    try:
        key = _load_private_key(pem_path)
    except ValueError as e:
        print(f'\033[91m.pem 키 로드 실패: {e}\033[0m')
        input('\033[0m계속하려면 엔터를 눌러주세요. ')
        return

    node_ips = [ip.strip() for ip in data['cicd_cache_node_ip'].split(',') if ip.strip()]
    node_port = int(data.get('cicd_cache_node_port', 22))
    for ip in node_ips:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(ip, port=node_port, username=data['cicd_cache_node_id'], pkey=key)
            _, stdout, stderr = client.exec_command(
                f'sudo rm -rf /CICD-DATA/local/{organization_name}-cicd /CICD-DATA/store/{organization_name}-cicd'
                f' && sudo mkdir -p /CICD-DATA/local/{organization_name}-cicd /CICD-DATA/store/{organization_name}-cicd'
            )
            exit_status = stdout.channel.recv_exit_status()
            if exit_status != 0:
                err_msg = stderr.read().decode().strip()
                print(f'\033[91m[{ip}] 캐시 폴더 초기화 실패 (exit {exit_status}): {err_msg}\033[0m')
            else:
                print(f'\033[96m[{ip}] 캐시 폴더 초기화 완료\033[0m')
        except Exception as e:
            print(f'\033[91m[{ip}] SSH 연결 실패: {e}\033[0m')
        finally:
            client.close()
