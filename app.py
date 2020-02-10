import random
from flask import Flask, render_template, request, redirect, url_for, session
from flask_bootstrap import Bootstrap
from sql_operations import *
from forms.movies_form import MoviesForm, UserForm, RegisterForm, RateForm, DirectorForm, GenreForm
from models import *
from db import db_string, secret

app = Flask(__name__)
app.config['SECRET_KEY'] = secret
app.config["SQLALCHEMY_DATABASE_URI"] = db_string
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
Bootstrap(app)

user_role = "NotAuthorized"
user_email = ""

@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        print(user_role)
        return render_template('index.html', role=user_role)

@app.route('/login', methods=['POST'])
def do_admin_login():
    user = get_data_by_email(User, request.form['email'])
    if user != None:
        if request.form['password'] == user.password and request.form['email'] == user.email:
            session['logged_in'] = True
            global user_role, user_email
            user_role = user.role.role_name
            user_email = user.email
    return index()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    error = ""
    if request.method == "POST" and form.validate_on_submit():
        print(form.email.data)
        if check_user_in_db(User, form.email.data) is None:
            user = User(user_id=int(random.getrandbits(31)), email=form.email.data, password=form.password.data,
                        date_of_birth=form.date_of_birth.data, role_id=3)
            insert_data(user)
            save()
            return redirect("/register")
        else:
            error = "Email already exists!"

    return render_template("register.html", form=form, error=error)

@app.route("/user", methods=["GET", "POST"])
def user():
     users = get_user_data(User)
     if user_role == "User":
         users = get_data_by_email(User, user_email)
     form = UserForm(request.form)
     if request.method == "POST" and form.validate_on_submit():
         roles = {"Admin" : 1, "Moderator" : 2, "User" : 3}
         role_id = roles[form.role_id.data]
         print(form.role_id)
         print(role_id)
         if check_user_in_db(User, form.email.data) is None:
             user = User(user_id = int(random.getrandbits(31)), email=form.email.data, password=form.password.data, date_of_birth=form.date_of_birth.data, role_id=role_id)
             insert_data(user)
         else:
             user = User(user_id=form.user_id.data, email=form.email.data, password=form.password.data, date_of_birth=form.date_of_birth.data, role_id=role_id)
             update_user(user, User)
         save()
         return redirect("/user")
     return render_template("user.html", users=users, form=form, role=user_role)


@app.route('/user/delete/<user_id>')
def user_delete(user_id):
    delete_user(User, user_id)
    save()
    return redirect('/user')


@app.route('/user/edit/<user_id>', methods=["GET"])
def user_edit(user_id):
    users = get_all_data(User)
    user = get_data_by_user_id(User, user_id)
    print(user_id)
    form = UserForm()
    if request.method == "GET":
        form.email.data = user.email
        form.password.data = user.password
        form.date_of_birth.data = user.date_of_birth
        form.role_id.data = user.role_id
        return render_template('user.html', users=users, form=form, role=user_role)

@app.route("/movies", methods=["GET", "POST"])
def movie():
    movies = get_all_data(Movie)
    form = MoviesForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        print(form.title.data)

        if check_movie_in_db(Movie, form.title.data) is None:
            movie = Movie(title=form.title.data, url=form.url.data, imdbrating=form.imdbrating.data,
                          ratingcount=form.ratingcount.data)
            insert_data(movie)
        else:
            movie = Movie(title=form.title.data, url=form.url.data, imdbrating=form.imdbrating.data,
                          ratingcount=form.ratingcount.data)
            update_movie(movie, Movie)
        save()
        return redirect("/movies")

    return render_template("movies.html", movies=movies, form=form, role=user_role)


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

@app.route('/movies/like/<title>')
def like(title):
    movie = get_data_by_title(Movie, title)
    user = get_data_by_email(User, user_email)
    user_movieq = get_user_movie(user_movie, user.user_id, movie.title)
    if user_movieq is None:
        record_to_db(user_movie, user.user_id, movie.title)
    return redirect('/movies')

@app.route('/favorites', methods=["GET", "POST"])
def favorites():
    form = RateForm()
    user = get_data_by_email(User, user_email)
    user_movies = get_all_user_movie(user_movie, user.user_id)
    if request.method == "POST" and form.validate_on_submit():
        update_user_movie(user_movie, rating=form.rating.data, title=form.title.data, user_id=form.user_id.data)
        return redirect('/favorites')
    return render_template('favorites.html', user_movies=user_movies, form=form)

@app.route('/favorites/rate/<title>', methods=["GET"])
def rate(title):
    user = get_data_by_email(User, user_email)
    user_movies = get_all_user_movie(user_movie, user.user_id)
    user_movieq = get_user_movie(user_movie, user.user_id, title)
    form = RateForm(request.form)
    if request.method == "GET":
        print(user_movieq)
        form.user_id.data = user_movieq.user_id
        form.title.data = title
        form.rating.data = user_movieq.user_rating
    return render_template('favorites.html', user_movies=user_movies, form=form, title=title)

@app.route('/favorites/delete/<title>', methods=["GET"])
def delete_user_mov(title):
    user = get_data_by_email(User, user_email)
    user_movieq = get_user_movie(user_movie, user.user_id, title)
    delete_user_movie(user_movie, user_movieq.user_id, title)
    save()
    return redirect('/favorites')

@app.route('/directors', methods=["GET", "POST"])
def directors():
    directors = get_all_directors(Director, Movie)
    form = DirectorForm()
    print(directors)
    if request.method == "POST" and form.validate_on_submit():
        if check_director_in_db(Director, form.director_id.data) is None:
            director = Director(first_name=form.first_name.data, last_name=form.last_name.data)
            insert_data(director)
        else:
            director = Director(director_id=form.director_id.data, first_name=form.first_name.data, last_name=form.last_name.data)
            update_director(director, Director)
        save()
        return redirect("/directors")
    return render_template('directors.html', directors=directors, role=user_role, form=form)

@app.route('/directors/delete/<director_id>')
def director_delete(director_id):
    delete_director(Director, director_id)
    save()
    return redirect('/directors')


@app.route('/directors/edit/<director_id>', methods=["GET"])
def director_edit(director_id):
    director = get_data_by_director_id(Director, director_id)
    directors = get_all_directors(Director, Movie)
    form = DirectorForm()
    if request.method == "GET":
        form.director_id.data = director.director_id
        form.first_name.data = director.first_name
        form.last_name.data = director.last_name
        return render_template('directors.html', directors=directors, form=form, role=user_role)


@app.route("/genres", methods=["GET", "POST"])
def genre():
    genres = get_all_data(Genre)
    form = GenreForm(request.form)
    # if request.method == "POST" and form.validate_on_submit():
    #
    #     if check_movie_in_db(Movie, form.title.data) is None:
    #         movie = Movie(title=form.title.data, url=form.url.data, imdbrating=form.imdbrating.data,
    #                       ratingcount=form.ratingcount.data)
    #         insert_data(movie)
    #     else:
    #         movie = Movie(title=form.title.data, url=form.url.data, imdbrating=form.imdbrating.data,
    #                       ratingcount=form.ratingcount.data)
    #         update_movie(movie, Movie)
    #     save()
    #     return redirect("/movies")

    return render_template("genres.html", genres=genres, form=form, role=user_role)

if __name__ == "__main__":
    app.run()
