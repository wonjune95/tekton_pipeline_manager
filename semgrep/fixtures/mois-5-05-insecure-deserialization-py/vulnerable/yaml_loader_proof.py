import yaml
import yaml.loader
from flask import Flask, request
from yaml import UnsafeLoader as UL

app = Flask(__name__)


class PluginLoader(yaml.Loader):
    """yaml.Loader 를 상속 — 이름에 Loader·Unsafe 가 없어도 임의 객체를 만든다"""


class TaggedSafeLoader(yaml.SafeLoader):
    """SafeLoader 를 상속했지만 생성자를 더할 수 있다"""


class SafeLoader(yaml.Loader):
    """이름만 SafeLoader 인 자체 클래스 (PyYAML 에서 import 한 것이 아니다)"""


TaggedSafeLoader.add_constructor("!run", lambda loader, node: __import__("os").system(loader.construct_scalar(node)))


@app.post("/config/import")
def import_config():
    text = request.get_data(as_text=True)
    # 위험한 이름 목록(Loader·UnsafeLoader·FullLoader)에 없다고 안전한 것이 아니다
    # ruleid: mois-5-05-insecure-deserialization-py
    a = yaml.load(text, Loader=PluginLoader)
    # import 별칭
    # ruleid: mois-5-05-insecure-deserialization-py
    b = yaml.load(text, Loader=UL)
    # 하위 모듈 경로로 적은 UnsafeLoader
    # ruleid: mois-5-05-insecure-deserialization-py
    c = yaml.load(text, Loader=yaml.loader.UnsafeLoader)
    # 위치 인자 + 하위 모듈 경로
    # ruleid: mois-5-05-insecure-deserialization-py
    d = yaml.load(text, yaml.loader.FullLoader)
    # 상속 클래스를 load_all 에
    # ruleid: mois-5-05-insecure-deserialization-py
    e = list(yaml.load_all(text, Loader=PluginLoader))
    # SafeLoader 를 상속한 클래스는 SafeLoader 가 아니다 (위에서 !run 생성자를 더했다)
    # ruleid: mois-5-05-insecure-deserialization-py
    f = yaml.load(text, Loader=TaggedSafeLoader)
    # 이름만 SafeLoader
    # ruleid: mois-5-05-insecure-deserialization-py
    g = yaml.load(text, Loader=SafeLoader)
    return {"n": len([a, b, c, d, e, f, g])}


@app.post("/config/dynamic")
def dynamic_loader(**options):
    text = request.get_data(as_text=True)
    # getattr 의 결과는 실행해 봐야 안다 (CLoader 가 없으면 Loader)
    # ruleid: mois-5-05-insecure-deserialization-py
    a = yaml.load(text, Loader=getattr(yaml, "CLoader", yaml.Loader))
    # 변수에 담은 Loader
    loader = yaml.Loader
    # ruleid: mois-5-05-insecure-deserialization-py
    b = yaml.load(text, Loader=loader)
    # 식 안에 SafeLoader 가 "들어 있을" 뿐, 요청 값에 따라 Loader 가 된다
    # ruleid: mois-5-05-insecure-deserialization-py
    c = yaml.load(text, Loader=yaml.SafeLoader if request.args.get("safe") else yaml.Loader)
    # ruleid: mois-5-05-insecure-deserialization-py
    d = yaml.load(text, Loader=(yaml.SafeLoader, yaml.Loader)[len(text) % 2])
    # 무엇이 들어올지 알 수 없는 **옵션
    # ruleid: mois-5-05-insecure-deserialization-py
    e = yaml.load(text, **options)
    return {"n": len([a, b, c, d, e])}
