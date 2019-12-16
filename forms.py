from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Optional, ValidationError
from user import is_username_taken


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])

    password = PasswordField("Password", validators=[DataRequired()])


class SignupForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])

    password = PasswordField("Password", validators=[DataRequired()])

    def validate_username(form, field):
        if "," in field.data or " " in field.data:
            raise ValidationError("Username error! (Can not include: (,) or space)")


class TaskEditForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])

    description = StringField("Description", validators=[Optional()])

    share = StringField("Share", validators=[Optional()])

    def validate_share(form, field):
        share = [x for x in field.data.split(",") if x != "" or x != " "]
        for username in share:
            if not (username == " " or username == ""):
                if not is_username_taken(username):
                    raise ValidationError("Username error!")


class ListEditForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])

    description = StringField("Description", validators=[Optional()])


