from flask import Flask, render_template, request
from sql_operations import get_all_data
from models import *
from db import db_string

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = db_string
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/movies")
def movie():
    movies = get_all_data(Movie)
    #movies = Movie.query.all()
    return render_template("movies.html", movies=movies)


if __name__ == "__main__":
    app.run()