import traceback

from django.http import HttpResponseBadRequest, HttpResponseServerError, JsonResponse
from fastapi import HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from flask import abort, flash, jsonify, make_response, redirect
from rest_framework.response import Response

from .services import run_report, save_order


# ---- 트레이스백 문자열을 응답 객체에 담는다 (return 과 다른 줄) ----
def django_trace(request):
    try:
        return run_report(request.user)
    except Exception:
        # ruleid: mois-4-01-error-message-exposure-py
        page = HttpResponseServerError(traceback.format_exc())
        # ruleid: mois-4-01-error-message-exposure-py
        body = JsonResponse({"trace": traceback.format_exc()}, status=500)
        return body if request.headers.get("Accept") == "application/json" else page


def drf_trace(request):
    try:
        return run_report(request.user)
    except Exception:
        # ruleid: mois-4-01-error-message-exposure-py
        resp = Response({"detail": traceback.format_exc()}, status=500)
        return resp


def fastapi_trace(kind: str):
    try:
        return run_report(kind)
    except KeyError:
        # ruleid: mois-4-01-error-message-exposure-py
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    except ValueError:
        # ruleid: mois-4-01-error-message-exposure-py
        resp = JSONResponse(content={"trace": traceback.format_exc()}, status_code=500)
        return resp
    except OSError:
        # ruleid: mois-4-01-error-message-exposure-py
        resp = PlainTextResponse(traceback.format_exc(), status_code=500)
        return resp
    except Exception:
        # ruleid: mois-4-01-error-message-exposure-py
        resp = HTMLResponse("<pre>" + traceback.format_exc() + "</pre>", status_code=500)
        return resp


def flask_trace(kind):
    try:
        return run_report(kind)
    except KeyError:
        # ruleid: mois-4-01-error-message-exposure-py
        payload = jsonify(trace=traceback.format_exc())
        return payload, 500
    except ValueError:
        # ruleid: mois-4-01-error-message-exposure-py
        resp = make_response(traceback.format_exc(), 500)
        return resp
    except OSError:
        # ruleid: mois-4-01-error-message-exposure-py
        abort(500, traceback.format_exc())
    except Exception:
        # ruleid: mois-4-01-error-message-exposure-py
        flash(traceback.format_exc())
        return redirect("/reports")


# ---- 잡은 예외를 응답 객체에 담는다 (return 과 다른 줄) ----
def django_error(request, order):
    try:
        save_order(order)
    except ValueError as e:
        # ruleid: mois-4-01-error-message-exposure-py
        page = HttpResponseBadRequest(e)
        return page
    except OSError as e:
        # ruleid: mois-4-01-error-message-exposure-py
        body = JsonResponse({"error": e.strerror}, status=500)
        return body
    return JsonResponse({"saved": True})


def drf_error(request, order):
    try:
        save_order(order)
    except ValueError as e:
        # ruleid: mois-4-01-error-message-exposure-py
        resp = Response({"detail": e.args}, status=400)
        return resp
    return Response(status=204)


def fastapi_error(order: dict):
    try:
        save_order(order)
    except KeyError as exc:
        # ruleid: mois-4-01-error-message-exposure-py
        resp = JSONResponse({"detail": exc.args}, status_code=400)
        return resp
    except ValueError as exc:
        # ruleid: mois-4-01-error-message-exposure-py
        resp = PlainTextResponse(exc.args[0], status_code=400)
        return resp
    except OSError as exc:
        # ruleid: mois-4-01-error-message-exposure-py
        resp = HTMLResponse("<p>" + exc.strerror + "</p>", status_code=500)
        return resp
    return {"saved": True}


def flask_error(order):
    try:
        save_order(order)
    except KeyError as exc:
        # ruleid: mois-4-01-error-message-exposure-py
        payload = jsonify(error=exc.args)
        return payload, 400
    except ValueError as exc:
        # ruleid: mois-4-01-error-message-exposure-py
        resp = make_response(exc.args[0], 400)
        return resp
    except PermissionError as exc:
        # ruleid: mois-4-01-error-message-exposure-py
        abort(403, exc.strerror)
    except OSError as exc:
        # ruleid: mois-4-01-error-message-exposure-py
        flash(exc.strerror)
        return redirect("/orders")
    except Exception as exc:
        # 예외 문자열을 본문으로 돌려준다
        # ruleid: mois-4-01-error-message-exposure-py
        return str(exc), 500
    return "saved"
