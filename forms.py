from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Optional


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])

    password = PasswordField("Password", validators=[DataRequired()])


class SignupForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])

    password = PasswordField("Password", validators=[DataRequired()])


class TaskEditForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])

    description = StringField("Description", validators=[Optional()])


class ListEditForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])

    description = StringField("Description", validators=[Optional()])


