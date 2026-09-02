"""04.gitea-source 의 istio 템플릿 렌더 검증.

    python3 test_istio_templates.py

egress_hosts 가 비었을 때 egress 리소스가 안 나오고, 값이 있으면
호스트 수만큼 라우팅이 생기는지만 본다. 나머지 gitops 템플릿은 기존과 동일해서 제외.
"""
import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = './04.gitea-source'
ENVS = ('dev', 'stg', 'prod')
BASE = {
    'application_name': 'sample-app',
    'organization_name': 'sample',
    'image_registry': 'registry.example.com',
}


def render(rel, data):
    j2 = Environment(loader=FileSystemLoader(ROOT), autoescape=False)
    return list(yaml.safe_load_all(j2.get_template(rel).render(data)))


def kinds(docs):
    return [d['kind'] for d in docs if d]


for env in ENVS:
    data = dict(BASE, **{f'{e}_{s}_domain_name': f'{e}-{s}.example.com'
                         for e in ENVS for s in ('frontend', 'backend')})

    fe = render(f'sample-frontend-istio-gitops/overlays/{env}/istio.yaml', data)
    assert kinds(fe) == ['Gateway', 'VirtualService', 'DestinationRule'], kinds(fe)
    srv = fe[0]['spec']['servers'][0]
    assert srv['port']['number'] == 80 and 'tls' not in srv, srv
    assert fe[1]['spec']['http'][0]['route'][0]['destination']['port']['number'] == 80
    assert f'{env}-frontend.example.com' in srv['hosts'][0]

    # egress_hosts 키가 없는 구 프로젝트 → 렌더가 깨지지 않고 인그레스만
    be = render(f'sample-backend-istio-gitops/overlays/{env}/istio.yaml', data)
    assert kinds(be) == ['Gateway', 'VirtualService', 'DestinationRule'], kinds(be)
    assert be[1]['spec']['http'][0]['route'][0]['destination']['port']['number'] == 8080

    # egress_hosts 2개 → 인그레스 + 이그레스 4종
    hosts = ['api.example.com', 'obs.example.com']
    be = render(f'sample-backend-istio-gitops/overlays/{env}/istio.yaml',
                dict(data, **{f'{e}_egress_hosts': hosts for e in ENVS}))
    assert kinds(be) == ['Gateway', 'VirtualService', 'DestinationRule',
                         'ServiceEntry', 'Gateway', 'DestinationRule',
                         'VirtualService'], kinds(be)
    se, egw, evs = be[3], be[4], be[6]
    assert se['spec']['hosts'] == hosts
    assert se['spec']['ports'][0] == {'number': 80, 'name': 'http', 'protocol': 'HTTP'}
    assert egw['spec']['selector'] == {'istio': 'egressgateway'}
    assert egw['spec']['servers'][0]['port']['protocol'] == 'HTTP'
    assert egw['spec']['servers'][0]['hosts'] == hosts
    # 1단계(mesh→egressgw) 1개 + 2단계(egressgw→외부) 호스트당 1개
    assert len(evs['spec']['http']) == 1 + len(hosts), evs['spec']['http']
    assert evs['spec']['http'][0]['match'][0]['gateways'] == ['mesh']
    assert evs['spec']['http'][0]['route'][0]['destination']['port']['number'] == 80
    for h, rule in zip(hosts, evs['spec']['http'][1:]):
        assert rule['match'][0]['authority']['exact'] == h, rule
        assert rule['route'][0]['destination']['host'] == h
        assert rule['route'][0]['destination']['port']['number'] == 80

print('istio 템플릿 렌더 OK (dev/stg/prod, egress 유/무)')
