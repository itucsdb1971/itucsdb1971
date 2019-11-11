from flask import Flask
import views, dbinit
from database import Database
from flask_login import LoginManager
from user import get_user

lm = LoginManager()


@lm.user_loader
def load_user(user_id):
    return get_user(user_id)


def create_app():
    app = Flask(__name__)
    if app.env == 'production':
        app.config.from_object('settings.ProductionConfig')
    else:
        app.config.from_object('settings.DevelopmentConfig')

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule(
        "/login", view_func=views.login_page, methods=["GET", "POST"]
    )
    app.add_url_rule("/logout", view_func=views.logout_page)
    app.add_url_rule(
        "/tasks", view_func=views.tasks_page, methods=["GET", "POST"]
    )
    app.add_url_rule("/tasks/<int:task_key>", view_func=views.task_page)
    app.add_url_rule(
        "/new-task", view_func=views.task_add_page, methods=["GET", "POST"]
    )
    app.add_url_rule(
        "/tasks/<int:task_key>/edit", view_func=views.task_edit_page, methods=["GET", "POST"]
    )

    lm.init_app(app)
    lm.login_view = "login_page"

    dbinit.run(app.config["DATABASE_URL"])
    db = Database(app.config["DATABASE_URL"])
    app.config["db"] = db

    return app


if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)
