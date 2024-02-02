from sqlalchemy import Column, Integer, String, Date, LargeBinary, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import base64

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password_hash = Column(String)
    is_admin = Column(Boolean)
    postcards = relationship('Postcard', backref="owner")


class Postcard(Base):
    __tablename__ = 'postcards'
    id = Column(Integer, primary_key=True)
    city = Column(String)
    country = Column(String)
    date = Column(Date)
    from_whom = Column(String)
    photo = Column(LargeBinary)
    owner_name = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))

    def to_json(self):
        return {
            'id': self.id,
            'city': self.city,
            'country': self.country,
            'date': self.date,
            'from_whom': self.from_whom,
            'photo': base64.b64encode(self.photo).decode('utf-8'),
            'owner_name': self.owner_name,
            'owner_id': self.owner_id
        }
# odkodowaniena bajdy
# decoded_data = base64.b64decode(your_image_string.encode('utf-8'))
