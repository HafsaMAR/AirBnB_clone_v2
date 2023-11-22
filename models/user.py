#!/usr/bin/python3
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, backref
from os import getenv

class User(BaseModel, Base):
    """User class representing the 'users' table in the database."""

    __tablename__ = 'users'
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        place = relationship('Place', backref='user')
        reviews = relationship('Review', backref='user')
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
