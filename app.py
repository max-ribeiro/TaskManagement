from flask import Flask, render_template, request

app = Flask(__name__)
tasks = []


@app.route("/")
def index():
    return render_template("index.html", tasks=tasks, title="Task Manager - Home")

@app.route("/add", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        tasks.append(request.form.get("task"))

    return render_template("addtask.html", title="Task Manager - Add Task")

