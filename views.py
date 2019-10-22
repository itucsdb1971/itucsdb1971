from flask import render_template, current_app, abort, request, redirect, url_for
from datetime import datetime
from movie import Movie
from forms import MovieEditForm


def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)


def movies_page():
    db = current_app.config["db"]
    if request.method == "GET":
        movies = db.get_movies()
        return render_template("movies.html", movies=sorted(movies))
    else:
        form_movie_keys = request.form.getlist("movie_keys")
        for form_movie_key in form_movie_keys:
            db.delete_movie(int(form_movie_key))
        return redirect(url_for("movies_page"))


def movie_page(movie_key):
    db = current_app.config["db"]
    movie = db.get_movie(movie_key)
    if movie is None:
        abort(404)
    return render_template("movie.html", movie=movie)


def movie_add_page():
    if request.method == "GET":
        values = {"title": "", "year": ""}
        return render_template(
            "movie_edit.html",
            min_year=1887,
            max_year=datetime.now().year,
            values=values,
        )
    else:
        valid = validate_movie_form(request.form)
        if not valid:
            return render_template(
                "movie_edit.html",
                min_year=1887,
                max_year=datetime.now().year,
                values=request.form,
            )
        title = request.form.data["title"]
        year = request.form.data["year"]
        movie = Movie(title, year=year)
        db = current_app.config["db"]
        movie_key = db.add_movie(movie)
        return redirect(url_for("movie_page", movie_key=movie_key))


def movie_edit_page(movie_key):
    if request.method == "GET":
        db = current_app.config["db"]
        movie = db.get_movie(movie_key)
        if movie is None:
            abort(404)
        values = {"title": movie.title, "year": movie.year}
        return render_template(
            "movie_edit.html",
            min_year=1887,
            max_year=datetime.now().year,
            values=values,
        )
    else:
        valid = validate_movie_form(request.form)
        if not valid:
            return render_template(
                "movie_edit.html",
                min_year=1887,
                max_year=datetime.now().year,
                values=request.form,
            )
        title = request.form.data["title"]
        year = request.form.data["year"]
        movie = Movie(title, year=year)
        db = current_app.config["db"]
        db.update_movie(movie_key, movie)
        return redirect(url_for("movie_page", movie_key=movie_key))


def movie_add_page():
    form = MovieEditForm()
    if form.validate_on_submit():
        title = form.data["title"]
        year = form.data["year"]
        movie = Movie(title, year=year)
        db = current_app.config["db"]
        movie_key = db.add_movie(movie)
        return redirect(url_for("movie_page", movie_key=movie_key))
    return render_template("movie_edit.html", form=form)


def movie_edit_page(movie_key):
    db = current_app.config["db"]
    movie = db.get_movie(movie_key)
    form = MovieEditForm()
    if form.validate_on_submit():
        title = form.data["title"]
        year = form.data["year"]
        movie = Movie(title, year=year)
        db.update_movie(movie_key, movie)
        return redirect(url_for("movie_page", movie_key=movie_key))
    form.title.data = movie.title
    form.year.data = movie.year if movie.year else ""
    return render_template("movie_edit.html", form=form)
