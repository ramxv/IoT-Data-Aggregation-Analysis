from flask import flask, request, render_template
import sqlite3

app = Flask(__name__)


@app.route("/")
def main_app():
    return render_template("index.html")
