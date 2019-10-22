from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, NumberRange, Optional
from wtforms_components import IntegerField

from datetime import datetime


class MovieEditForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])

    year = IntegerField(
        "Year",
        validators=[
            Optional(),
            NumberRange(min=1887, max=datetime.now().year),
        ],
    )
