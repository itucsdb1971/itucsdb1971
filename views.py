from flask import render_template, current_app, abort, request, redirect, url_for, flash
from datetime import datetime
from task import Task
from forms import TaskEditForm, LoginForm
from flask_login import login_user, logout_user, current_user, login_required
from user import get_user
from passlib.hash import pbkdf2_sha256 as hasher


def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)


def tasks_page():
    db = current_app.config["db"]
    if request.method == "GET":
        tasks = db.get_tasks()
        return render_template("tasks.html", tasks=sorted(tasks))
    else:
        if not current_user.is_admin:
            abort(401)
        form_task_keys = request.form.getlist("task_keys")
        for form_task_key in form_task_keys:
            db.delete_task(int(form_task_key))
        flash("%(num)d tasks deleted." % {"num": len(form_task_keys)})
        return redirect(url_for("tasks_page"))


def task_page(task_key):
    db = current_app.config["db"]
    task = db.get_task(task_key)
    if task is None:
        abort(404)
    return render_template("task.html", task=task)


@login_required
def task_add_page():
    if not current_user.is_admin:
        abort(401)
    form = TaskEditForm()
    if form.validate_on_submit():
        name = form.data["name"]
        description = form.data["description"]
        task = Task(name, description=description)
        db = current_app.config["db"]
        task_key = db.add_task(task)
        flash("Task added.")
        return redirect(url_for("task_page", task_key=task_key))
    return render_template("task_edit.html", form=form)


@login_required
def task_edit_page(task_key):
    db = current_app.config["db"]
    task = db.get_task(task_key)
    if task is None:
        abort(404)
    form = TaskEditForm()
    if form.validate_on_submit():
        name = form.data["name"]
        description = form.data["description"]
        task = Task(name, description=description)
        db.update_task(task_key, task)
        flash("Task data updated.")
        return redirect(url_for("task_page", task_key=task_key))
    form.name.data = task.name
    form.description.data = task.description if task.description else ""
    return render_template("task_edit.html", form=form)


def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.data["username"]
        user = get_user(username)
        if user is not None:
            password = form.data["password"]
            if hasher.verify(password, user.password):
                login_user(user)
                flash("You have logged in.")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
        flash("Invalid credentials.")
    return render_template("login.html", form=form)


def logout_page():
    logout_user()
    flash("You have logged out.")
    return redirect(url_for("home_page"))
