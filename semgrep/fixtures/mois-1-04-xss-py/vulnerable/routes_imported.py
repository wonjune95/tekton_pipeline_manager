"""다른 모듈에서 가져온 app (Flask 인지 FastAPI 인지 이 파일에서는 알 수 없다) — 태그가 들어간 문자열 반환은 탐지한다."""
from flask import request

from myproject.web import app


@app.post("/comments")
def post_comment():
    body = request.form["body"]
    # ruleid: mois-1-04-xss-py
    return f"<p class='comment'>{body}</p>"


@app.put("/profile")
def put_profile():
    nickname = request.form["nickname"]
    # ruleid: mois-1-04-xss-py
    return "<span>" + nickname + "</span> 님의 정보를 저장했습니다"


@app.patch("/profile")
def patch_profile():
    bio = request.form["bio"]
    # ruleid: mois-1-04-xss-py
    return "<blockquote>%s</blockquote>" % bio


@app.delete("/comments")
def delete_comment():
    comment_id = request.args["id"]
    # ruleid: mois-1-04-xss-py
    return f"<p>댓글 {comment_id} 을(를) 삭제했습니다</p>"
