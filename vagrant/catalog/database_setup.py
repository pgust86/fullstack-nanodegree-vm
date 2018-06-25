from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()
# creates user class for each logged in user
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
#create class for different genres of movies
class Genres(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name'          :self.name,
            'id'            :self.id,
        }
#class for individual movies
class Movies(Base):
    __tablename__='movies'

    name = Column(String(150), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(500))
    rating = Column(String(6))
    poster_url = Column(String(250))
    genre_id = Column(Integer, ForeignKey('genres.id'))
    genre = relationship(Genres)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'name'          :self.name,
            'id'            :self.id,
            'descripton'            :self.description,
            'rating'            :self.rating,
            'poster_url'            :self.poster_url,
        }

engine = create_engine('sqlite:///moviescatalog.db')

Base.metadata.create_all(engine)
