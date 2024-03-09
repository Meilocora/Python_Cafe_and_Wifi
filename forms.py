from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


# WTForm for creating a cafe
class CreateCafeForm(FlaskForm):
    name = StringField("Name of the Cafe", validators=[DataRequired()])
    map_url = StringField("Cafe Map URL", validators=[DataRequired(), URL()])
    img_url = StringField("Cafe Image URL", validators=[DataRequired(), URL()])
    location = StringField("Location", validators=[DataRequired()])
    seats = StringField("Seats")
    coffee_price = StringField("Coffee Price")
    has_sockets = RadioField("Cafe has sockets", choices=[(False, "no"), (True, "yes")])
    has_toilet = RadioField("Cafe has a toilet", choices=[(False, "no"), (True, "yes")])
    has_wifi = RadioField("Cafe has Wifi", choices=[(False, "no"), (True, "yes")])
    can_take_calls = RadioField("Can take calls here", choices=[(False, "no"), (True, "yes")])
    submit = SubmitField("Add Cafe")



