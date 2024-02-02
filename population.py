from shered import User, Postcard, Base, PictureService

from PIL import Image
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date

import hashlib
import os

def hash_password_function(password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    password_hash = sha256.hexdigest()
    return password_hash

DATABASE_URL = 'sqlite:///restApiDb/myPostcards.db'

engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(engine)        # Dodanie klas do bazy

Session = sessionmaker(bind=engine)
session = Session()

# dodanie Admina
'''
name = "tkowa"
password = "admindupa"
is_admin = 1
password_hash = hash_password_function(password)
admin = User(name=name, password_hash=password_hash, is_admin=is_admin)
session.add(admin)
session.commit()
'''

# dadanie usera
'''
name = "kowal"
password = "qwerty1234"
is_admin = 0
password_hash = hash_password_function(password)
admin = User(name=name, password_hash=password_hash, is_admin=is_admin)
session.add(admin)
session.commit()
'''

# dadanie kartki dla usera tkowa
'''
username = "tkowa"
user = session.query(User).filter(User.name == username).first()
print(user.id)

pictureService = PictureService()
picture_data = pictureService.picture_to_bytes("./restApiDb/photos/london.jpg")
# print(london_data)
# image = pictureService.bytes_to_picture(london_data)
# image.save("london20.jpg")

city = "London"
country = "England"
date = date(2023, 9, 16)
from_whom = "Asia"
owner_id = user.id

postcard = Postcard(city=city, country=country, date=date,from_whom=from_whom,photo=picture_data, owner_id=owner_id)
session.add(postcard)
session.commit()
'''

# dodanie kartki dla usera kowal
'''
username = "kowal"
user = session.query(User).filter(User.name == username).first()
print(user.id)

pictureService = PictureService()
picture_data = pictureService.picture_to_bytes("./restApiDb/photos/valencia.jpg")
# print(london_data)
# image = pictureService.bytes_to_picture(london_data)
# image.save("london20.jpg")

city = "Valencia"
country = "Spain"
date = date(2023, 11, 14)
from_whom = "Iza"
owner_id = user.id

postcard = Postcard(city=city, country=country, date=date,from_whom=from_whom,photo=picture_data, owner_id=owner_id)
session.add(postcard)
session.commit()
'''

