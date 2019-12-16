from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, IntegerField
from wtforms.validators import DataRequired, Optional, ValidationError, InputRequired
from user import is_username_taken


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])

    password = PasswordField("Password", validators=[DataRequired()])


class SignupForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])

    password = PasswordField("Password", validators=[DataRequired()])

    def validate_username(form, field):
        if len(field.data) >= 80:
            raise ValidationError("Username too long!")

        if "," in field.data or " " in field.data:
            raise ValidationError("Username error! (Can not include: (,) or space)")


class TaskEditForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])

    description = StringField("Description", validators=[Optional()])

    share = StringField("Share", validators=[Optional()])

    deadline = DateField("Deadline", validators=[Optional()])

    status = IntegerField("Status", validators=[InputRequired()])

    assign = StringField("Assign", validators=[Optional()])

    location = StringField("Location", validators=[Optional()])

    def validate_name(form, field):
        if len(field.data) >= 80:
            raise ValidationError("Username too long!")

    def validate_description(form, field):
        if len(field.data) >= 80:
            raise ValidationError("Description too long!")

    def validate_share(form, field):
        share = [x for x in field.data.split(",") if x != "" or x != " "]
        for username in share:
            if not (username == " " or username == ""):
                if not is_username_taken(username):
                    raise ValidationError("Username error!")


class ListEditForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])

    description = StringField("Description", validators=[Optional()])

    def validate_name(form, field):
        if len(field.data) >= 80:
            raise ValidationError("Username too long!")

    def validate_description(form, field):
        if len(field.data) >= 80:
            raise ValidationError("Description too long!")


