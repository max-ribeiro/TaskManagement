from datetime import timedelta, datetime
import uuid
from flask import Blueprint, render_template, request, url_for, redirect, current_app

pages = Blueprint("tasks", __name__, template_folder="templates", static_folder="static")

# creates a global datesRange variable that can be accessed in all aplication templates
@pages.context_processor
def add_calc_date_range():
    def dateRange(start: datetime):
        print(start)
        dates = [start + timedelta(days=diff) for diff in range(-3, 4)]
        return dates

    return{"dateRange": dateRange}

def today_at_midnight():
    today = datetime.today()
    return datetime(today.year, today.month, today.day)

@pages.route("/")
def index():
    dateString = request.args.get("date")
    if dateString:
        selectedDate = datetime.fromisoformat(dateString)
    else:
        selectedDate = today_at_midnight()

    tasksOnDate = current_app.db.tasks.find({"added":{"$lte": selectedDate}})
    completions = [
        task["task"]
        for task in  current_app.db.completions.find({"date": selectedDate})
    ]

    return render_template(
        "index.html",
        tasks=tasksOnDate,
        title="Task Manager - Home",
        selectedDate=selectedDate,
        completions=completions
    )

@pages.route("/add", methods=["GET", "POST"])
def add_task():
    today = today_at_midnight()

    if request.method == "POST":
        task = request.form.get("task")
        current_app.db.tasks.insert_one({
            "_id": uuid.uuid4().hex,
            "added": today,
            "name": task
        })

    return render_template("addtask.html", title="Task Manager - Add Task", selectedDate=today)

@pages.post("/complete")
def complete():
    dateString = request.form.get("date")
    task = request.form.get("taskId")
    date = datetime.fromisoformat(dateString)
    current_app.db.completions.insert_one({"date": date, "task": task})
    # completions[someDate].append(task)

    return redirect(url_for("tasks.index", date=dateString))