from flask import Flask, request, session
from flask.views import MethodView

app = Flask(__name__)


@app.route("/search")
def search():
    last_query = request.args.get("q", "")
    return {"q": last_query}


class NoteAPI(MethodView):
    methods = ["PUT"]

    def put(self, note_id):
        drafts = session.setdefault("drafts", {})
        drafts[str(note_id)] = request.get_json()
        session.modified = True
        return {"saved": note_id}


app.add_url_rule("/notes/<int:note_id>", view_func=NoteAPI.as_view("note"))
