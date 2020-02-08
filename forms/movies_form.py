from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, FloatField


class MoviesForm(FlaskForm):

   title = StringField("Title: ", [
        validators.DataRequired("Please enter url"),
   ])

   url = StringField("URL: ",
        [validators.DataRequired("Minimal work expirience required")]
    )

   imdbrating = FloatField("IMDB Rating: ", [
       validators.DataRequired("Please enter your birthday."),
       validators.length(4, 60, "Pleas select between 4 to 60")
   ])

   ratingcount = FloatField("Rating Count: ", [
       validators.DataRequired("Please enter topic."),
       validators.length(10, 100, "Pleas select between 10 to 100")
    ])

   submit = SubmitField("Save")