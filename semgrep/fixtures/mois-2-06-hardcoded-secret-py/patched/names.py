# 값이 비밀이 아니라 필드·헤더·쿠키·인증 방식의 "이름"인 상수.
# 이름이 password·secret·token·key 로 끝나도 값이 이런 낱말 그 자체면 탐지하지 않는다 (한 줄에 낱말 하나)

# ok: mois-2-06-hardcoded-secret-py OAuth grant_type 값
OAUTH_GRANT_PASSWORD = "password"
# ok: mois-2-06-hardcoded-secret-py 옛 스키마의 컬럼 이름
COLUMN_PASSWD = "passwd"
# ok: mois-2-06-hardcoded-secret-py Vault KV 엔진의 기본 마운트 이름
VAULT_MOUNT_SECRET = "secret"
# ok: mois-2-06-hardcoded-secret-py OAuth response_type 값
RESPONSE_TYPE_TOKEN = "token"
# ok: mois-2-06-hardcoded-secret-py 질의 매개변수 이름
QUERY_PARAM_API_KEY = "api_key"
QUERY_PARAM_ACCESS_KEY = "accessKey"
# ok: mois-2-06-hardcoded-secret-py 값을 읽어 올 환경변수 이름
ENV_NAME_SECRET_KEY = "SECRET_KEY"
# ok: mois-2-06-hardcoded-secret-py Authorization 헤더의 방식 이름
SCHEME_FOR_TOKEN = "Bearer"
SCHEME_FOR_PASSWORD = "Basic"
# ok: mois-2-06-hardcoded-secret-py 쿠키·폼 필드 이름
COOKIE_CSRF_TOKEN = "csrftoken"
FIELD_CSRF_TOKEN = "csrfmiddlewaretoken"
COOKIE_SESSION_TOKEN = "sessionid"
COOKIE_ACCESS_TOKEN = "access_token"
COOKIE_REFRESH_TOKEN = "refresh_token"
# ok: mois-2-06-hardcoded-secret-py 헤더 이름
HEADER_API_KEY = "X-API-Key"


def password_widget(show_password, toggle_password, saved_password, column_password):
    # ok: mois-2-06-hardcoded-secret-py 비밀번호 값이 아니라 표시 여부·입력 종류·빈 값 표시·컬럼 이름과의 비교
    if show_password == "false":
        return {"type": "password"}
    if toggle_password == "text":
        return {"type": "text"}
    if toggle_password == "hidden":
        return {"type": "hidden"}
    if toggle_password == "password":
        return {"type": "password"}
    if saved_password == "None":
        return {"type": "password", "value": ""}
    if saved_password == "null":
        return {"type": "password", "value": ""}
    if column_password == "passwd":
        return {"type": "password", "name": "passwd"}
    return {"type": "password", "name": "password"}
