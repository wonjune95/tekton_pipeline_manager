import importlib

from django.http import JsonResponse


def calculate(request):
    expr = request.GET.get("expr", "")
    # 외부 입력을 그대로 eval 로 실행
    # ruleid: mois-1-02-code-injection-py
    result = eval(expr)
    return JsonResponse({"result": result})


def run_plugin(request):
    name = request.POST["plugin"]
    # 외부 입력으로 모듈을 동적 import
    # ruleid: mois-1-02-code-injection-py
    module = importlib.import_module("plugins." + name)
    return JsonResponse({"output": module.run()})
