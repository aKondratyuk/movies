from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

user_movie = db.Table("user_movie",
                      db.Column("user_id", db.Integer, db.ForeignKey("user.user_id"), primary_key=True),
                      db.Column("title", db.String(255), db.ForeignKey("movie.title"), primary_key=True),
                      db.Column("user_rating", db.Float(10), nullable=True))


movie_genre = db.Table("movie_genre",
                      db.Column("title", db.String(255), db.ForeignKey("movie.title"), primary_key=True),
                      db.Column("genre_id", db.Integer, db.ForeignKey("genre.genre_id"), primary_key=True))


class Genre(db.Model):
    __tablename__ = "genre"
    genre_id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(255), nullable=False, unique=True)

    movies = db.relationship("Movie", secondary=movie_genre)

    def __init__(self, genre_id, genre_name):
        self.genre_id = genre_id
        self.genre_name = genre_name


class Movie(db.Model):
    __tablename__ = "movie"
    title = db.Column(db.String(255), primary_key=True)
    url = db.Column(db.String(1255), nullable=False, unique=True)
    imdbrating = db.Column(db.Float(10), nullable=False)
    ratingcount = db.Column(db.Float(10), nullable=False)
    director_id = db.Column(db.Integer, db.ForeignKey("director.director_id"), nullable=True)

    director = db.relationship("Director", backref="movie", lazy=True)
    users = db.relationship("User", secondary=user_movie)
    genres = db.relationship("Genre", secondary=movie_genre)

    def __init__(self, title, url, imdbrating, ratingcount):
        self.title = title
        self.url = url
        self.imdbrating = imdbrating
        self.ratingcount = ratingcount


class Director(db.Model):
    __tablename__ = "director"
    director_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)

    def __init__(self, director_id, first_name, last_name):
        self.director_id = director_id
        self.first_name = first_name
        self.last_name = last_name


class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(2000), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.role_id"), nullable=False)

    role = db.relationship("Role", backref="user")
    movies = db.relationship('Movie', secondary=user_movie)

    def __init__(self, user_id, email, password, date_of_birth):
        self.user_id = user_id
        self.email = email
        self.password = password
        self.date_of_birth = date_of_birth


class Role(db.Model):
    __tablename__ = "role"
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(255), nullable=False)

    def __init__(self, role_id, role_name):
        self.role_id = role_id
        self.role_name = role_name