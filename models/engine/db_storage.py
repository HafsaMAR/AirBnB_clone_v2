#!/usr/bin/python3
"""this is the dbstorage engine """

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


classname = {"User": User, "State": State, "City": City,
             "Amenity": Amenity, "Place": Place, "Review": Review}


class DBStorage:
    """Database storage class."""

    __engine = None
    __session = None

    def __init__(self):
        """Create  the base class"""
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST', default='localhost')
        db = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')

        self.__engine = create_engine(
            f"mysql+mysqldb://{user}:{password}@{host}/{db}",
            pool_pre_ping=True)

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

    def all(self, cls=None):
        """function to list all ojbect"""
        result_dict = {}
        for class_name, class_type in classname.items():
            if cls is None or cls is class_type:
                query_result = self.__session.query(class_type).all()
                for obj in query_result:
                    key = f"{class_name}.{obj.id}"
                    result_dict[key] = obj

        return result_dict

    def new(self, obj):
        """function  to add and cmmit """
        self.__session.add(obj)

    def save(self):
        """the save method in the DBstorage class"""
        self.__session.commit()

    def delete(self, obj=None):
        """function to delete"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """function to reload objects"""
        Base.metadata.create_all(self.__engine)
        session_maker = sessionmaker(bind=self.__engine, expire_on_commi=False)
        Session = scoped_session(session_maker)
        self.__session = Session
