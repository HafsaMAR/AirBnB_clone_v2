#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DATETIME, func

from os import getenv
if getenv('HBNB_TYPE_STORAGE') == "db":
    Base = declarative_base()
else:
    Base = object
class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), primary_key = True, unique=True, nullable=True)
    created_at = Column(DATETIME, nullable=True, default=datetime.utcnow())
    updated_at = Column(DATETIME, nullable=True, default=datetime.utcnow())
    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

        else:
            # Check if 'created_at' and 'updated_at' keys are present
            self.id = str(uuid.uuid4())

            if 'created_at' not in kwargs:
                kwargs['created_at'] = datetime.now()

            kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],'%Y-%m-%dT%H:%M:%S.%f')
            kwargs['created_at'] = datetime.strptime(kwargs['created_at'],'%Y-%m-%dT%H:%M:%S.%f')
            if '__class__' in kwargs:
                del kwargs['__class__']
            self.__dict__.update(kwargs)


    def __str__(self):
        """String representation"""
        return '[{}] ({}) {}'.format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        for key, value in self.__dict__.items():
            if key != '_sa_instance_state':
                dictionary[key] = value

        dictionary.update({'__class__':
                      (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary
        
    def delete(self):
        ''' Delete the current instance from the storage '''
        from models import storage
        storage.delete(self)
