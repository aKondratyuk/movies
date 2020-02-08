from db import engine, Base, Session
from sqlalchemy.orm.attributes import InstrumentedAttribute

Base.metadata.create_all(engine)

session = Session()

def check_movie_in_db(class_name, arg):
    title = session.query(class_name).filter_by(title=arg).first()
    return title


def get_all_data(class_name):
    return session.query(class_name).all()


def get_data_by_id(class_name, id):
    return session.query(class_name).filter_by(id=int(id)).first()


def get_data_by_title(class_name, title):
    return session.query(class_name).filter_by(title=title).first()


def insert_data(data):
    session.add(data)


def update_data(obj, class_name):
    mapped_values = {}
    for item in class_name.__dict__.items():
        field_name = item[0]
        field_type = item[1]
        is_column = isinstance(field_type, InstrumentedAttribute)
        if is_column:
            mapped_values[field_name] = getattr(obj, field_name)

    session.query(class_name).filter_by(id=obj.id).update(mapped_values)


def update_movie(obj, class_name):
    mapped_values = {}
    for item in class_name.__dict__.items():
        field_name = item[0]
        field_type = item[1]
        is_column = isinstance(field_type, InstrumentedAttribute)
        if is_column:
            mapped_values[field_name] = getattr(obj, field_name)

    movie = session.query(class_name).filter(class_name.title == mapped_values['title']).one()
    movie.title = mapped_values['title']
    movie.url = mapped_values['url']
    movie.imdbrating = mapped_values['imdbrating']
    movie.ratingcount = mapped_values['ratingcount']


def delete_movie(class_name, title):
    movie = session.query(class_name).filter_by(title=title).first()
    session.delete(movie)

def delete_data(class_name, id):
    user = session.query(class_name).filter_by(id=id).first()
    session.delete(user)


def save():
    session.commit()