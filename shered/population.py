from models import User, Postcard, Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import hashlib
import os

def hash_password_function(password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    password_hash = sha256.hexdigest()
    return password_hash

DATABASE_URL = 'sqlite:///restApiDb/myPostcards.db'

engine = create_engine(DATABASE_URL, echo=True)  # You can change the database URL accordingly
Base.metadata.create_all(engine)

# Session = sessionmaker(bind=engine)
# session = Session()
#
# # dodanie Admina
# name = "tkowa"
# password = "admindupa"
# is_admin = 1
# password_hash = hash_password_function(password)
# admin = User(name=name, password_hash=password_hash, is_admin=is_admin)
# session.add(admin)
# session.commit()
