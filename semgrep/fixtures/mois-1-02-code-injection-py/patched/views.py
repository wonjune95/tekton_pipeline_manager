import ast
import importlib

from django.http import HttpResponseBadRequest, JsonResponse

ALLOWED_PLUGINS = {"report": "plugins.report", "export": "plugins.export"}


def calculate(request):
    expr = request.GET.get("expr", "")
    try:
        # ok: mois-1-02-code-injection-py 리터럴(숫자·목록)만 해석하고 코드는 실행하지 않음
        result = ast.literal_eval(expr)
    except (ValueError, SyntaxError):
        return HttpResponseBadRequest("invalid expression")
    return JsonResponse({"result": result})


def run_plugin(request):
    # ok: mois-1-02-code-injection-py 허용 목록(dict)에 있는 모듈만 import
    module_name = ALLOWED_PLUGINS.get(request.POST.get("plugin", ""))
    if module_name is None:
        return HttpResponseBadRequest("unknown plugin")
    module = importlib.import_module(module_name)
    return JsonResponse({"output": module.run()})
