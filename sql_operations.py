from db import engine, Base, Session

Base.metadata.create_all(engine)

session = Session()

def get_all_data(class_name):
    return session.query(class_name).all()