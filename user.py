from flask import current_app
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.active = True

    def get_id(self):
        return self.username

    @property
    def is_active(self):
        return self.active


def get_user(username):
    db = current_app.config["db"]
    user = db.get_user(username)
    return user


def create_user(username, password):
    db = current_app.config["db"]
    db.add_user(username, password)
    return


def is_username_taken(username):
    db = current_app.config["db"]
    return db.is_username_taken(username)
