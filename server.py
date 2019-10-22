from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)


@app.route("/movies")
def movies_page():
    return render_template("movies.html")


if __name__ == "__main__":
    app.run()
