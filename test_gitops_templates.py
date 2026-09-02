"""04.gitea-source GitOps 템플릿 + 메뉴 4 연동 검증.

    python3 test_gitops_templates.py

프레임워크 없이 assert 로만 돌린다. kubectl 이 있으면 kustomize build 까지 확인하고,
없으면 그 항목만 건너뛴다.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

import yaml
from jinja2 import Environment, FileSystemLoader

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

ROOT = './04.gitea-source'
TOML = './00.reset/tekton_init.toml'
MENU4 = './menu/menu4_add_gitops.py'
ENVS = ('dev', 'stg', 'prod')

_failed = []


def check(name):
    """테스트 데코레이터. 실패해도 나머지를 계속 돌린다."""
    def deco(fn):
        try:
            fn()
        except AssertionError as e:
            _failed.append((name, str(e) or 'assert 실패'))
            print(f'  \033[91mFAIL\033[0m {name}\n        {e}')
        except Exception as e:
            _failed.append((name, f'{type(e).__name__}: {e}'))
            print(f'  \033[91mERR \033[0m {name}\n        {type(e).__name__}: {e}')
        else:
            print(f'  \033[92mok  \033[0m {name}')
        return fn
    return deco


def base_data(**over):
    """실제 toml 값 + 렌더에 필요한 앱/조직명."""
    with open(TOML, 'rb') as f:
        d = dict(tomllib.load(f))
    d.update(application_name='sample-app', organization_name='sample')
    d.update(over)
    return d


def render(rel, data):
    j2 = Environment(loader=FileSystemLoader(ROOT), autoescape=False)
    return [d for d in yaml.safe_load_all(j2.get_template(rel).render(data)) if d]


def templates():
    return sorted(d for d in os.listdir(ROOT)
                  if d.startswith('sample-') and d.endswith('-gitops'))


def kinds(docs):
    return [d['kind'] for d in docs]


# ── 1. 설정 파일 ────────────────────────────────────────
@check('tekton_init.toml 파싱 및 istio 키 존재')
def _():
    d = base_data()
    for e in ENVS:
        k = f'{e}_egress_hosts'
        assert k in d, f'{k} 없음'
        assert isinstance(d[k], list) and d[k], f'{k} 는 비어있지 않은 배열이어야 함: {d[k]!r}'
        for e2 in ('frontend', 'backend'):
            assert f'{e}_{e2}_domain_name' in d


# ── 2. 전체 템플릿 렌더 ─────────────────────────────────
@check('템플릿 10종 × 환경 3개 모두 유효한 YAML 로 렌더')
def _():
    tops = templates()
    assert len(tops) == 10, f'템플릿 개수 {len(tops)}: {tops}'
    data = base_data()
    for top in tops:
        for root, _dirs, files in os.walk(os.path.join(ROOT, top)):
            for fn in files:
                rel = os.path.relpath(os.path.join(root, fn), ROOT)
                docs = render(rel, data)
                for d in docs:
                    assert 'kind' in d, f'{rel}: kind 없음'
                    if d['kind'] != 'Kustomization':
                        assert 'metadata' in d, f'{rel}: metadata 없음'


# ── 3. kustomize build ──────────────────────────────────
@check('kustomize build 30/30 (템플릿 10종 × 환경 3개)')
def _():
    if not shutil.which('kubectl'):
        print('        (kubectl 없음 — 건너뜀)')
        return
    data = base_data()
    j2 = Environment(loader=FileSystemLoader(ROOT), autoescape=False)
    with tempfile.TemporaryDirectory() as out:
        for top in templates():
            for root, _dirs, files in os.walk(os.path.join(ROOT, top)):
                for fn in files:
                    rel = os.path.relpath(os.path.join(root, fn), ROOT)
                    dst = os.path.join(out, rel)
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    with open(dst, 'w') as f:
                        f.write(j2.get_template(rel).render(data))
        for top in templates():
            for env in ENVS:
                p = os.path.join(out, top, 'overlays', env)
                r = subprocess.run(['kubectl', 'kustomize', p],
                                   capture_output=True, text=True)
                assert r.returncode == 0, f'{top}/{env}: {r.stderr.strip()[:200]}'


# ── 4. 프론트 istio ─────────────────────────────────────
@check('frontend-istio: Gateway 80/HTTP + VS + DR, TLS 없음')
def _():
    for env in ENVS:
        docs = render(f'sample-frontend-istio-gitops/overlays/{env}/istio.yaml', base_data())
        assert kinds(docs) == ['Gateway', 'VirtualService', 'DestinationRule'], kinds(docs)
        gw, vs, dr = docs
        srv = gw['spec']['servers'][0]
        assert gw['spec']['selector'] == {'istio': 'ingressgateway'}
        assert srv['port'] == {'number': 80, 'name': 'http', 'protocol': 'HTTP'}, srv['port']
        assert 'tls' not in srv, 'TLS 설정이 남아있음'
        assert vs['spec']['http'][0]['route'][0]['destination'] == {
            'host': 'sample-app-svc', 'port': {'number': 80}}
        assert dr['spec']['trafficPolicy']['loadBalancer']['consistentHash']['httpCookie']['name'] == 'route'


# ── 5. 백엔드 istio: 인그레스 + 이그레스 ────────────────
@check('backend-istio: 인그레스 3종 + 이그레스 4종 생성')
def _():
    for env in ENVS:
        docs = render(f'sample-backend-istio-gitops/overlays/{env}/istio.yaml', base_data())
        assert kinds(docs) == ['Gateway', 'VirtualService', 'DestinationRule',
                               'ServiceEntry', 'Gateway', 'DestinationRule',
                               'VirtualService'], kinds(docs)
        gw, vs = docs[0], docs[1]
        assert gw['spec']['servers'][0]['port']['number'] == 80
        assert vs['spec']['http'][0]['route'][0]['destination']['port']['number'] == 8080


@check('backend-istio egress: 호스트 개수만큼 라우팅, 전부 평문 HTTP')
def _():
    hosts = ['api.example.com', 'obs.example.com', 'files.example.com']
    for env in ENVS:
        data = base_data(**{f'{e}_egress_hosts': hosts for e in ENVS})
        se, egw, edr, evs = render(
            f'sample-backend-istio-gitops/overlays/{env}/istio.yaml', data)[3:]
        assert se['spec']['hosts'] == hosts
        assert se['spec']['location'] == 'MESH_EXTERNAL'
        assert se['spec']['ports'][0] == {'number': 80, 'name': 'http', 'protocol': 'HTTP'}
        assert egw['spec']['selector'] == {'istio': 'egressgateway'}
        assert egw['spec']['servers'][0]['port']['protocol'] == 'HTTP'
        assert egw['spec']['servers'][0]['hosts'] == hosts
        assert edr['spec']['host'] == 'istio-egressgateway.istio-system.svc.cluster.local'
        assert edr['spec']['subsets'] == [{'name': 'external'}]
        assert evs['spec']['gateways'] == ['mesh', 'sample-app-egress-gw']
        rules = evs['spec']['http']
        assert len(rules) == 1 + len(hosts), f'라우팅 {len(rules)}개'
        # 1단계: mesh -> egress gateway
        assert rules[0]['match'][0]['gateways'] == ['mesh']
        assert rules[0]['route'][0]['destination']['host'].startswith('istio-egressgateway.')
        # 2단계: egress gateway -> 외부, Host 헤더로 대상 구분
        for h, r in zip(hosts, rules[1:]):
            assert r['match'][0]['gateways'] == ['sample-app-egress-gw']
            assert r['match'][0]['authority']['exact'] == h
            assert r['route'][0]['destination'] == {'host': h, 'port': {'number': 80}}


@check('backend-istio: egress 키가 없는 구 init_result.json 에서도 렌더 성공')
def _():
    data = base_data()
    for e in ENVS:
        data.pop(f'{e}_egress_hosts', None)
    for env in ENVS:
        docs = render(f'sample-backend-istio-gitops/overlays/{env}/istio.yaml', data)
        assert kinds(docs) == ['Gateway', 'VirtualService', 'DestinationRule'], kinds(docs)


# ── 6. istio 템플릿에 남으면 안 되는 것 ─────────────────
@check('istio 템플릿에 Ingress / TLS 잔재 없음')
def _():
    bad = re.compile(r'kind:\s*Ingress|ingressClassName|networking\.k8s\.io|'
                     r'credentialName|secret-tls|protocol:\s*(TLS|HTTPS)')
    for top in ('sample-frontend-istio-gitops', 'sample-backend-istio-gitops'):
        for root, _dirs, files in os.walk(os.path.join(ROOT, top)):
            for fn in files:
                p = os.path.join(root, fn)
                with open(p, encoding='utf-8') as f:
                    for i, line in enumerate(f, 1):
                        if line.lstrip().startswith('#'):
                            continue
                        assert not bad.search(line), f'{p}:{i} {line.strip()}'


# ── 7. HPA ──────────────────────────────────────────────
@check('HPA scaleTargetRef 가 실제 존재하는 워크로드를 가리킴')
def _():
    for top in templates():
        for env in ENVS:
            hpa = os.path.join(ROOT, top, 'overlays', env, 'hpa.yaml')
            if not os.path.exists(hpa):
                continue
            doc = render(os.path.relpath(hpa, ROOT), base_data())[0]
            ref = doc['spec']['scaleTargetRef']
            has_rollout = os.path.exists(os.path.join(ROOT, top, 'overlays', env, 'rollout.yaml'))
            want = ('argoproj.io/v1alpha1', 'Rollout') if has_rollout else ('apps/v1', 'Deployment')
            assert (ref['apiVersion'], ref['kind']) == want, \
                f'{top}/{env}: rollout.yaml {"있음" if has_rollout else "없음"} 인데 {ref}'


@check('HPA 에 autoscaling/v1 전용 필드 없음')
def _():
    for top in templates():
        for env in ENVS:
            hpa = os.path.join(ROOT, top, 'overlays', env, 'hpa.yaml')
            if not os.path.exists(hpa):
                continue
            doc = render(os.path.relpath(hpa, ROOT), base_data())[0]
            assert doc['apiVersion'] == 'autoscaling/v2', doc['apiVersion']
            assert 'targetCPUUtilizationPercentage' not in doc['spec'], f'{top}/{env}'
            assert doc['spec']['metrics'], f'{top}/{env}: metrics 없음'


# ── 8. 메뉴 4 연동 ──────────────────────────────────────
@check('메뉴 4: 선택 번호 ↔ 템플릿 폴더 매핑 일치')
def _():
    full = open(MENU4, encoding='utf-8').read()
    src = full[full.index('def choice_gitops'):full.index('def create_registry')]
    sl = re.search(r'selection_list = \[(.*?)\n    \]', src, re.S).group(1)
    items = [m.group(1) for m in re.finditer(r"'([^']*)',", sl)]
    keys = [(k, n) for k, n in
            re.findall(r"\{'key':\s*'(\d+)',\s*'name':\s*'(\w+)'", src) if k != '0']
    nums = [int(k) for k, _ in keys]
    assert nums == list(range(1, len(items))), f'메뉴 번호 {nums}'
    for k, name in keys:
        want = items[int(k)]
        assert want.startswith(name.lower()), f'{k}번 {name} -> {want}'
        assert os.path.isdir(os.path.join(ROOT, f'sample-{want}-gitops')), \
            f'{k}번 {want}: 템플릿 폴더 없음'
    assert 'if int(choice) == 0:' in src, '뒤로가기가 0 이 아님'
    assert re.search(r"\{'key':\s*'0',\s*'name':\s*'뒤로가기'", src), '뒤로가기 항목 없음'


@check('메뉴 4: init_result.json 에 없는 toml 키를 보충')
def _():
    src = open(MENU4, encoding='utf-8').read()
    assert 'setdefault' in src and 'tekton_init.toml' in src, '보충 로직 없음'
    found = [j for j in
             (os.path.join(r, f) for r, _d, fs in os.walk('result') for f in fs)
             if j.endswith('-init_result.json')] if os.path.isdir('result') else []
    if not found:
        print('        (init_result.json 없음 — 실제 병합 검증 건너뜀)')
        return
    data = json.load(open(found[0]))
    with open(TOML, 'rb') as f:
        for k, v in tomllib.load(f).items():
            data.setdefault(k, v)
    data.update(application_name='sample-app', organization_name='sample')
    for env in ENVS:
        docs = render(f'sample-backend-istio-gitops/overlays/{env}/istio.yaml', data)
        assert 'ServiceEntry' in kinds(docs), f'{env}: 보충 후에도 egress 없음'


# ── 9. 네임스페이스 사이드카 주입 라벨 ──────────────────
@check('클러스터 yaml 12개에 istio-injection 라벨')
def _():
    dirs = ['01.init', '02-1.add-storage-in-organization']
    n = 0
    for d in dirs:
        for fn in sorted(os.listdir(d)):
            if not fn.endswith('-cluster.yaml'):
                continue
            docs = [x for x in yaml.safe_load_all(
                open(os.path.join(d, fn), encoding='utf-8').read()
                .replace('{{', 'X').replace('}}', 'X')) if x]
            ns = [x for x in docs if x.get('kind') == 'Namespace']
            assert ns, f'{d}/{fn}: Namespace 없음'
            for x in ns:
                labels = x['metadata'].get('labels') or {}
                assert labels.get('istio-injection') == 'enabled', f'{d}/{fn}'
            n += 1
    assert n == 12, f'클러스터 yaml {n}개 (12개 기대)'


if __name__ == '__main__':
    print(f'\n{len(_failed)} 실패' if _failed else '\n\033[92m전체 통과\033[0m')
    sys.exit(1 if _failed else 0)
