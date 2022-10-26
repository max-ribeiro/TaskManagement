from datetime import timedelta, date
from collections import defaultdict
from flask import Blueprint, render_template, request, url_for, redirect

pages = Blueprint("tasks", __name__, template_folder="templates", static_folder="static")
tasks = ["some task"]
completions = defaultdict(list)

# creates a global datesRange variable that can be accessed in all aplication templates
@pages.context_processor
def add_calc_date_range():
    def dateRange(start: date):
        print(start)
        dates = [start + timedelta(days=diff) for diff in range(-3, 4)]
        return dates

    return{"dateRange": dateRange}

@pages.route("/")
def index():
    dateString = request.args.get("date")
    if dateString:
        selectedDate = date.fromisoformat(dateString)
    else:
        selectedDate = date.today()
    return render_template(
        "index.html",
        tasks=tasks,
        title="Task Manager - Home",
        selectedDate=selectedDate,
        completions=completions[selectedDate]
    )

@pages.route("/add", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        tasks.append(request.form.get("task"))

    return render_template("addtask.html", title="Task Manager - Add Task", selectedDate=date.today())

@pages.post("/complete")
def complete():
    dateString = request.form.get("date")
    task = request.form.get("taskName")
    someDate = date.fromisoformat(dateString)
    completions[someDate].append(task)

    return redirect(url_for("tasks.index", date=dateString))