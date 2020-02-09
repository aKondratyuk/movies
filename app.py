import random
from flask import Flask, render_template, request, redirect, url_for, session
from flask_bootstrap import Bootstrap
from sql_operations import *
from forms.movies_form import MoviesForm, UserForm
from models import *
from db import db_string, secret

app = Flask(__name__)
app.config['SECRET_KEY'] = secret
app.config["SQLALCHEMY_DATABASE_URI"] = db_string
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
Bootstrap(app)

user_role = "User"

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

    if request.form['password'] == user.password and request.form['email'] == user.email:
        session['logged_in'] = True
        global user_role
        user_role = user.role.role_name
    return index()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()


@app.route("/user", methods=["GET", "POST"])
def user():
     users = get_user_data(User)
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

     return render_template("user.html", users=users, form=form)


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
        return render_template('user.html', users=users, form=form)

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
