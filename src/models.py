from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    # Here we define columns for the table planets
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    population = Column(Integer, nullable=False)
    diameter = Column(Integer, nullable=False)
    climate = Column(String(250), nullable=False)
    orbital_period = Column(Integer, nullable=False)
    rotation_period = Column(Integer, nullable=False)
    gravity = Column(String(250), nullable=False)
    terrain = Column(String(250), nullable=False)
    surface_water = Column(Integer, nullable=False)

    def serialize(self):
        return {}

class Characters(db.Model):
    __tablename__ = 'characters'
    # Here we define columns for the table characters
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    birth_year = Column(String(250), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year
        }

class Favorites(db.Model):
    __tablename__ = 'favorites'
    # Here we define columns for the table favorites
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User")
    planet_id = Column(Integer, ForeignKey('planets.id'))
    planet = relationship("Planets")
    character_id = Column(Integer, ForeignKey('characters.id'))
    character = relationship("Characters") 
    
    
    


    def serialize(self):
        return {}