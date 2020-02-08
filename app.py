from flask import Flask, render_template, request, redirect, url_for
from sql_operations import get_all_data, get_data_by_id, get_data_by_title, insert_data, update_data, delete_data, \
    save, update_movie, delete_movie, check_movie_in_db
from forms.movies_form import MoviesForm
from models import *
from db import db_string, secret

app = Flask(__name__)
app.config['SECRET_KEY'] = secret
app.config["SQLALCHEMY_DATABASE_URI"] = db_string
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/movies", methods=["GET", "POST"])
def movie():
    movies = get_all_data(Movie)
    form = MoviesForm(request.form)
    if request.method == "POST":
        print(form.title.data)

        if check_movie_in_db(Movie, form.title.data) == None:
            movie = Movie(title=form.title.data, url=form.url.data, imdbrating=form.imdbrating.data, ratingcount=form.ratingcount.data)
            insert_data(movie)
        else:
            movie = Movie(title=form.title.data, url=form.url.data, imdbrating=form.imdbrating.data, ratingcount=form.ratingcount.data)
            update_movie(movie, Movie)
        save()
        return redirect("/movies")

    return render_template("movies.html", movies=movies, form=form)


@app.route('/movies/delete/<title>')
def movie_delete(title):
    delete_movie(Movie, title)
    save()
    return redirect('/movies')


@app.route('/movies/edit/<title>', methods=["GET"])
def movie_edit(title):
    movie = get_data_by_title(Movie, title)
    print(title)
    print(movie.url)
    print(movie)
    movies = get_all_data(Movie)
    form = MoviesForm()
    if request.method == "GET":
        form.title.data = movie.title
        form.url.data = movie.url
        form.imdbrating.data = movie.imdbrating
        form.ratingcount.data = movie.ratingcount
        return render_template('movies.html', movies=movies, form=form)


if __name__ == "__main__":
    app.run()