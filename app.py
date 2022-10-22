from crypt import methods
from turtle import title
from flask import Flask, render_template

app = Flask(__name__)

def render():
    @app.route("/")
    def index():
        return render_template("index.html", title="Task Manager - Home")

    @app.route("/add", methods=["GET", "POST"])
    def add_habit():
        return render_template("addtask.html", title="Task Manager - Add Task")

    return app