from flask import Flask, request
from flask.views import MethodView

app = Flask(__name__)
last_query = ""


@app.route("/search")
def search():
    global last_query
    # ruleid: mois-6-01-shared-field-in-singleton-py
    last_query = request.args.get("q", "")  # 전역 변수에 요청별 검색어 저장
    return {"q": last_query}


class NoteAPI(MethodView):
    drafts = {}

    def put(self, note_id):
        # ruleid: mois-6-01-shared-field-in-singleton-py
        self.drafts[note_id] = request.get_json()  # 클래스 속성 dict 를 요청마다 변경
        return {"saved": note_id}


app.add_url_rule("/notes/<int:note_id>", view_func=NoteAPI.as_view("note"))
