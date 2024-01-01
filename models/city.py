#!/usr/bin/python3
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from os import getenv


class City(BaseModel, Base):
    """City class representing the 'cities' table in the database."""

    __tablename__ = 'cities'
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'cities'
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        place = relationship('Place', backref='cities')
    else:
        state_id = ""
        name = ""