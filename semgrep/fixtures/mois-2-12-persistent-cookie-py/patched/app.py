from datetime import timedelta

from flask import Flask

app = Flask(__name__)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
