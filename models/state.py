#!/usr/bin/python3

""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
from models.city import City

st_type = getenv('HBNB_TYPE_STORAGE')


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    if st_type == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state',
                              cascade='all, delete', passive_deletes=True)
    else:
        name = ''

        @property
        def cities(self):
            list_instance = []
            from models import storage
            cities = storage.all(City)
            for city in cities.values():
                if city.state_id == self.id:
                    list_instance.append(city)
            return list_instance