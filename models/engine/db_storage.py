#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import Base

un = os.getenv('HBNB_MYSQL_USER')  # un=username
pwd = os.getenv('HBNB_MYSQL_PWD')
host = os.getenv('HBNB_MYSQL_HOST')
db = os.getenv('HBNB_MYSQL_DB')
env = os.getenv('HBNB_ENV')


class DBStorage:
    """This class manages storage of hbnb databases"""
    __engine = None
    __session = None

    def __init__(self):
        """DBStorage Inits"""
        self.__engine = create_engine(
                'mysql+mysqldb://{}:{}@{}:3306/{}'
                .format(un, pwd, host, db),
                pool_pre_ping=True)
        if env == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """Query on the current database session
        all objects depending of the class name
        """
        from models.amenity import Amenity
        from models.city import City
        from models.place import Place
        from models.review import Review
        from models.state import State
        from models.user import User

        if cls:
            one_cls = {}
            all_obj = self.__session.query(cls).all()
            for obj in all_obj:
                one_cls.update({type(obj).__name__ + "." + obj.id: obj})
            return one_cls
        elif cls==None:
            all_cls = {}
            amenity_obj = self.__session.query(Amenity).all()
            for obj in amenity_obj:
                all_cls.update({type(obj).__name__ + "." + obj.id: obj})

            city_obj = self.__session.query(City).all()
            for obj in city_obj:
                all_cls.update({type(obj).__name__ + "." + obj.id: obj})

            place_obj = self.__session.query(cls).all()
            for obj in place_obj:
                all_cls.update({type(obj).__name__ + "." + obj.id: obj})

            review_obj = self.__session.query(Review).all()
            for obj in review_obj:
                all_cls.update({type(obj).__name__ + "." + obj.id: obj})

            state_obj = self.__session.query(State).all()
            for obj in state_obj:
                all_cls.update({type(obj).__name__ + "." + obj.id: obj})

            user_obj = self.__session.query(cls).all()
            for obj in user_obj:
                all_cls.update({type(obj).__name__ + "." + obj.id: obj})

            return all_cls
    
    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj"""
        if obj:
            self.__session.delete(obj)
    
    def reload(self):
        """create all tables in the database"""
        from models.amenity import Amenity
        from models.city import City
        from models.place import Place
        from models.review import Review
        from models.state import State
        from models.user import User

        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
