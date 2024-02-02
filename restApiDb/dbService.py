from datetime import datetime

from shered import User, Postcard, TokenService

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import hashlib, base64

DATABASE_URL = 'sqlite:///restApiDb/myPostcards.db'
ps = Postcard()

class DbService:
    def __init__(self):
        self.tokenService = TokenService()
        engine = create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=engine)

    @staticmethod
    def hash_password(password):
        sha256 = hashlib.sha256()
        sha256.update(password.encode('utf-8'))
        password_hash = sha256.hexdigest()
        return password_hash

    def login(self, username, password):
        session = self.Session()
        user = session.query(User).filter(User.name == username).first()
        if not user:
            return 0

        password_hash = self.hash_password(password)
        if user.password_hash != password_hash:
            return 0

        token = self.tokenService.generate_jwt_token(user.id, user.name, user.is_admin)
        session.close()
        return token

    def login_google(self, name, email):
        session = self.Session()
        user = session.query(User).filter(User.name == name, User.email == email).first()
        if not user:
            user_new = User(name=name, email=email, is_admin=0)
            session.add(user_new)
            session.commit()
        user = session.query(User).filter(User.name == name, User.email == email).first()

        token = self.tokenService.generate_jwt_token(user.id, user.name, user.is_admin)
        session.close()
        return token

    def create_postcard(self, city, country, date, from_whom, photo, token):
        user = self.tokenService.verify_jwt_token(token)
        if user == 0:
            # trzeba się zalogować
            return 0, ps

        photo_bytes = base64.b64decode(photo.encode('utf-8'))
        date_obj = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S GMT').date()
        session = self.Session()
        postcard = Postcard(city=city,
                            country=country,
                            date=date_obj,
                            from_whom=from_whom,
                            photo=photo_bytes,
                            owner_id=user['user_id'],
                            )
        postcard.owner_name = user['username']
        session.add(postcard)
        session.commit()
        postcard_json = postcard.to_json()
        session.close()
        return 1, postcard_json

    def get_all_postcards(self, token):
        user = self.tokenService.verify_jwt_token(token)
        if user == 0:
            # trzeba się zalogować
            return 0, []
        if not user['is_admin']:
            # tylko admin moze
            return 0, []
        session = self.Session()
        postcards = session.query(Postcard).all()
        postcards_json = []
        for postcard in postcards:
            user = session.query(User).filter(User.id == postcard.owner_id).first()
            postcard.owner_name = user.name
            # print(postcard.to_json())
            postcards_json.append(postcard.to_json())
        session.commit()
        session.close()
        return 1, postcards_json

    def get_user_postcards(self, token):
        user = self.tokenService.verify_jwt_token(token)
        if user == 0:
            # trzeba się zalogować
            return 0, []
        session = self.Session()
        postcards = session.query(Postcard).filter(Postcard.owner_id == user['user_id']).all()
        postcards_json = []
        for postcard in postcards:
            postcards_json.append(postcard.to_json())
        session.close()
        return 1, postcards_json

    def get_single_postcard(self, postcard_id, token):

        user = self.tokenService.verify_jwt_token(token)
        if user == 0:
            # trzeba się zalogować
            return 0, ps
        session = self.Session()
        postcard = session.query(Postcard).filter(Postcard.id == postcard_id).first()
        if not postcard:
            # nie ma w db
            return -1, ps
        if postcard.owner_id != user['user_id'] and not user['is_admin']:
            # nie kartka usera i nie admin
            return 0, ps
        return 1, postcard.to_json()

    def update_postcard(self, postcard_id, city, country, date, from_whom, photo, token):
        user = self.tokenService.verify_jwt_token(token)
        if user == 0:
            # trzeba się zalogować
            return 0, ps
        session = self.Session()
        postcard = session.query(Postcard).filter(Postcard.id == postcard_id).first()
        if not postcard:
            # nie ma w db
            return -1, ps
        if postcard.owner_id != user['user_id'] and not user['is_admin']:
            # nie kartka usera i nie admin
            return 0, ps
        date_obj = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S GMT').date()
        photo_bytes = base64.b64decode(photo.encode('utf-8'))

        postcard.city = city
        postcard.country = country
        postcard.date = date_obj
        postcard.from_whom = from_whom
        postcard.photo = photo_bytes
        session.commit()
        postcard_json = postcard.to_json()
        session.close()
        return 1, postcard_json

    def delete_postcard(self, postcard_id, token):
        user = self.tokenService.verify_jwt_token(token)
        if user == 0:
            # trzeba się zalogować
            return 0
        session = self.Session()
        postcard = session.query(Postcard).filter(Postcard.id == postcard_id).first()
        if not postcard:
            # nie ma w db
            return -1
        if postcard.owner_id != user['user_id'] and not user['is_admin']:
            # nie kartka usera i nie admin
            return
        session.delete(postcard)
        session.commit()
        session.close()
        return 1
