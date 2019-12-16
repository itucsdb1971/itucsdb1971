from flask import render_template, current_app, abort, request, redirect, url_for, flash
from datetime import datetime
from task import Task
from list import List
from forms import TaskEditForm, ListEditForm, LoginForm, SignupForm
from flask_login import login_user, logout_user, current_user, login_required
from user import get_user, create_user, is_username_taken
from passlib.hash import pbkdf2_sha256 as hasher


def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)


@login_required
def tasks_page():
    db = current_app.config["db"]
    if request.method == "GET":
        tasks = db.get_tasks(current_user.username)
        shared_tasks = []
        for task in tasks[:]:
            if db.count_task_user_relation(task[0])[0] >= 2:
                tasks.remove(task)
                shared_tasks.append(task)
        return render_template("tasks.html", tasks=sorted(tasks), shared_tasks=sorted(shared_tasks))
    else:
        form_task_keys = request.form.getlist("task_keys")
        for form_task_key in form_task_keys:
            task = db.get_task(form_task_key, current_user.username)
            if task is None:
                abort(404)
            db.delete_task(int(form_task_key))
        flash("%(num)d tasks deleted." % {"num": len(form_task_keys)})
        return redirect(url_for("tasks_page"))


@login_required
def task_page(task_key):
    db = current_app.config["db"]
    task = db.get_task(task_key, current_user.username)
    if task is None:
        abort(404)
    task_share = db.get_task_share(task_key)
    if len(task_share) <= 1:
        task_share = None
    else:
        task_share = sorted(task_share)
    return render_template("task.html", task=task, task_share=task_share)


@login_required
def task_add_page():
    form = TaskEditForm()
    if form.validate_on_submit():
        name = form.data["name"]
        description = form.data["description"]
        deadline = form.data["deadline"]
        task = Task(name, description=description, deadline=deadline)
        db = current_app.config["db"]
        task_key = db.add_task(task)
        db.add_task_user_relation(task_key, current_user.username)
        share = [x for x in form.data["share"].split(",") if x != "" and x != " "]
        for username in share:
            db.add_task_user_relation(task_key, username)
        flash("Task added.")
        return redirect(url_for("task_page", task_key=task_key))
    return render_template("task_edit.html", form=form)


@login_required
def task_edit_page(task_key):
    db = current_app.config["db"]
    task = db.get_task(task_key, current_user.username)
    if task is None:
        abort(404)
    form = TaskEditForm()
    if form.validate_on_submit():
        share = [x for x in form.data["share"].split(",") if x != "" and x != " "]
        db.delete_task_user_relation(task_key)
        for username in share:
            db.add_task_user_relation(task_key, username)
        if not db.is_exist_task_user_relation(task_key):
            db.delete_task(task_key)
        else:
            name = form.data["name"]
            description = form.data["description"]
            deadline = form.data["deadline"]
            task = Task(name, description=description, deadline=deadline)
            db.update_task(task_key, task)
        flash("Task data updated.")
        if current_user.username not in share:
            return redirect(url_for("tasks_page"))
        return redirect(url_for("task_page", task_key=task_key))
    form.name.data = task.name
    form.description.data = task.description if task.description else ""
    form.deadline.data = task.deadline if task.deadline else ""
    task_share = db.get_task_share(task_key)
    if len(task_share) < 1:
        task_share = None
    else:
        task_share = sorted(task_share)
    return render_template("task_edit.html", form=form, task_share=task_share)


@login_required
def lists_page():
    db = current_app.config["db"]
    if request.method == "GET":
        lists = db.get_lists(current_user.username)
        return render_template("lists.html", lists=sorted(lists))
    else:
        form_list_keys = request.form.getlist("list_keys")
        for form_list_key in form_list_keys:
            list = db.get_list(form_list_key, current_user.username)
            if list is None:
                abort(404)
            db.delete_list(int(form_list_key))
        flash("%(num)d lists deleted." % {"num": len(form_list_keys)})
        return redirect(url_for("lists_page"))


@login_required
def list_page(list_key):
    db = current_app.config["db"]
    if request.method == "GET":
        list = db.get_list(list_key, current_user.username)
        if list is None:
            abort(404)
        tasks = db.get_tasks_with_list(list_key)
        shared_tasks = []
        for task in tasks[:]:
            if db.count_task_user_relation(task[0])[0] >= 2:
                tasks.remove(task)
                shared_tasks.append(task)
        return render_template("list.html", list=list, tasks=sorted(tasks), shared_tasks=sorted(shared_tasks))
    else:
        form_task_keys = request.form.getlist("task_keys")
        if "remove" in request.form:
            for form_task_key in form_task_keys:
                task = db.get_task(form_task_key, current_user.username)
                if task is None:
                    abort(404)
                db.task_remove_list(int(form_task_key))
            flash("%(num)d tasks removed from this list." % {"num": len(form_task_keys)})
        elif "delete" in request.form:
            for form_task_key in form_task_keys:
                task = db.get_task(form_task_key, current_user.username)
                if task is None:
                    abort(404)
                db.delete_task(int(form_task_key))
            flash("%(num)d tasks deleted." % {"num": len(form_task_keys)})
        return redirect(url_for("list_page", list_key=list_key))


@login_required
def list_add_page():
    form = ListEditForm()
    if form.validate_on_submit():
        name = form.data["name"]
        description = form.data["description"]
        list = List(name, description=description)
        db = current_app.config["db"]
        list_key = db.add_list(list)
        db.add_list_user_relation(list_key, current_user.username)
        flash("List added.")
        return redirect(url_for("list_page", list_key=list_key))
    return render_template("list_edit.html", form=form)


@login_required
def list_edit_page(list_key):
    db = current_app.config["db"]
    list = db.get_list(list_key, current_user.username)
    if list is None:
        abort(404)
    form = ListEditForm()
    if form.validate_on_submit():
        name = form.data["name"]
        description = form.data["description"]
        list = List(name, description=description)
        db.update_list(list_key, list)
        flash("List data updated.")
        return redirect(url_for("list_page", list_key=list_key))
    form.name.data = list.name
    form.description.data = list.description if list.description else ""
    return render_template("list_edit.html", form=form)


@login_required
def list_new_task_page(list_key):
    form = TaskEditForm()
    if form.validate_on_submit():
        name = form.data["name"]
        description = form.data["description"]
        deadline = form.data["deadline"]
        task = Task(name, description=description, list_id=list_key, deadline=deadline)
        db = current_app.config["db"]
        task_key = db.add_task_with_list(task)
        db.add_task_user_relation(task_key, current_user.username)
        share = [x for x in form.data["share"].split(",") if x != "" and x != " "]
        for username in share:
            db.add_task_user_relation(task_key, username)
        flash("Task added.")
        return redirect(url_for("list_page", list_key=list_key))
    return render_template("task_edit.html", form=form)


@login_required
def list_add_task_page(list_key):
    db = current_app.config["db"]
    if request.method == "GET":
        tasks = db.get_tasks(current_user.username)
        shared_tasks = []
        for task in tasks[:]:
            if db.count_task_user_relation(task[0])[0] >= 2:
                tasks.remove(task)
                shared_tasks.append(task)
        return render_template("add_task_to_list.html", tasks=sorted(tasks), shared_tasks=sorted(shared_tasks))
    else:
        form_task_keys = request.form.getlist("task_keys")
        for form_task_key in form_task_keys:
            db.task_add_list(list_key, form_task_key)
        flash("%(num)d tasks added to this list." % {"num": len(form_task_keys)})
        return redirect(url_for("list_page", list_key=list_key))


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


def signup_page():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.data["username"]
        if not is_username_taken(username):
            password = form.data["password"]
            create_user(username, hasher.encrypt(password))
            flash("You have successfully created an account.")
            next_page = request.args.get("next", url_for("login_page"))
            return redirect(next_page)
        flash("Username taken.")
    return render_template("signup.html", form=form)
