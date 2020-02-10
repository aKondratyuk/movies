from sqlalchemy import and_

from db import engine, Base, Session
from sqlalchemy.orm.attributes import InstrumentedAttribute

Base.metadata.create_all(engine)

sessionq = Session()

def check_movie_in_db(class_name, arg):
    title = sessionq.query(class_name).filter_by(title=arg).first()
    return title

def check_user_in_db(class_name, arg):
    user = sessionq.query(class_name).filter_by(email=arg).first()
    return user

def get_all_data(class_name):
    return sessionq.query(class_name).all()

def get_user_data(class_name):
    return sessionq.query(class_name).join(class_name.role)

def get_data_by_user_id(class_name, user_id):
    return sessionq.query(class_name).filter_by(user_id=int(user_id)).first()

def get_data_by_email(class_name, email):
    return sessionq.query(class_name).filter_by(email=email).join(class_name.role).first()

def get_data_by_id(class_name, id):
    return sessionq.query(class_name).filter_by(id=int(id)).first()


def get_data_by_title(class_name, title):
    return sessionq.query(class_name).filter_by(title=title).first()


def insert_data(data):
    sessionq.add(data)


def update_data(obj, class_name):
    mapped_values = {}
    for item in class_name.__dict__.items():
        field_name = item[0]
        field_type = item[1]
        is_column = isinstance(field_type, InstrumentedAttribute)
        if is_column:
            mapped_values[field_name] = getattr(obj, field_name)

    sessionq.query(class_name).filter_by(id=obj.id).update(mapped_values)


def update_user(obj, class_name):
    mapped_values = {}
    for item in class_name.__dict__.items():
        field_name = item[0]
        field_type = item[1]
        is_column = isinstance(field_type, InstrumentedAttribute)
        if is_column:
            mapped_values[field_name] = getattr(obj, field_name)

    user = sessionq.query(class_name).filter(class_name.email == mapped_values['email']).one()
    user.email = mapped_values['email']
    user.password = mapped_values['password']
    user.date_of_birth = mapped_values['date_of_birth']
    user.role_id = mapped_values['role_id']

def update_movie(obj, class_name):
    mapped_values = {}
    for item in class_name.__dict__.items():
        field_name = item[0]
        field_type = item[1]
        is_column = isinstance(field_type, InstrumentedAttribute)
        if is_column:
            mapped_values[field_name] = getattr(obj, field_name)

    movie = sessionq.query(class_name).filter(class_name.title == mapped_values['title']).one()
    movie.title = mapped_values['title']
    movie.url = mapped_values['url']
    movie.imdbrating = mapped_values['imdbrating']
    movie.ratingcount = mapped_values['ratingcount']


def delete_movie(class_name, title):
    movie = sessionq.query(class_name).filter_by(title=title).first()
    sessionq.delete(movie)

def delete_user(class_name, user_id):
    user = sessionq.query(class_name).filter_by(user_id=user_id).first()
    sessionq.delete(user)

def delete_data(class_name, id):
    user = sessionq.query(class_name).filter_by(id=id).first()
    sessionq.delete(user)

def get_db_session_scope(sql_db_session):
    session = sql_db_session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def save():
    sessionq.commit()

def get_user_movie(class_name, user_id, title):
    return sessionq.query(class_name).filter_by(user_id=user_id, title=title).first()

def get_all_user_movie(class_name, user_id):
    return sessionq.query(class_name).filter_by(user_id=user_id).all()

def record_to_db(MyTable, user_id, title, rating=None):
    insert_stmnt = MyTable.insert().values(user_id=user_id, title=title, user_rating=rating)
    sessionq.execute(insert_stmnt)
    save()
    return

def delete_user_movie(MyTable, user_id, title):
    q = MyTable.delete().where(
       and_(
           MyTable.c.user_id == user_id,
           MyTable.c.title == title
       )
    )
    sessionq.execute(q)

def update_user_movie(MyTable, rating, title, user_id):
    delete_user_movie(MyTable, user_id, title)
    record_to_db(MyTable, user_id, title, rating)
    save()
    return
