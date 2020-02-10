from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, PasswordField, DateField, IntegerField, HiddenField, SelectField
from wtforms.validators import DataRequired, URL, Length, NumberRange, Email

class MoviesForm(FlaskForm):
    title = StringField("Title: ", validators=[DataRequired(), Length(1, 255, "Too long title!")])
    url = StringField("URL: ", validators=[DataRequired(), URL(), Length(1, 1255, "Too long url!")])
    imdbrating = FloatField("IMDB Rating: ", validators=[DataRequired(), NumberRange(0.0, 10.0, "Min rating 0 and max 10!")])
    ratingcount = FloatField("Rating Count: ", validators=[DataRequired()])
    submit = SubmitField("Save")


class UserForm(FlaskForm):
    user_id = HiddenField("Id")
    email = StringField("Email: ", validators=[DataRequired(), Length(1, 255, "Too long email!"), Email()])
    password = StringField("Password: ", validators=[DataRequired(), Length(1, 2000, "Too long password!")])
    date_of_birth = DateField("Birthday: ", validators=[DataRequired()])
    role_id = SelectField("Role: ", choices=[("Admin", "Admin"), ("Moderator", "Moderator"), ("User", "User")])
    submit = SubmitField("Save")

class RegisterForm(FlaskForm):
    user_id = HiddenField("Id")
    email = StringField("Email: ", validators=[DataRequired(), Length(1, 255, "Too long email!"), Email()])
    password = StringField("Password: ", validators=[DataRequired(), Length(1, 2000, "Too long password!")])
    date_of_birth = DateField("Birthday: ", validators=[DataRequired()])
    submit = SubmitField("Save")

