#!/usr/bin/python3
"""
Contains the class DBStorage
"""
import models
from models.base_model import BaseModel, Base
from models.author import Author
from models.book import Book
from models.category import Category
from models.publisher import Publisher
from models.order import Order
from models.user import User
from models.order_status import OrderStatus
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


classes = {
    'User': User,
    'Book': Book,
    'Category': Category,
    'Publisher': Publisher,
    'Order': Order,
    'OrderStatus': OrderStatus,
    'Author': Author
}


class DBStorage:
    """
    This class is the link
    between the ORM and the MySQL database
    """
    __engine = None
    __session = None

    def __init__(self):
        # the env has prefixed ONBST_ to the env variables
        ONBST_MYSQL_USER = getenv('ONBST_MYSQL_USER')
        ONBST_MYSQL_PWD = getenv('ONBST_MYSQL_PWD')
        ONBST_MYSQL_HOST = getenv('ONBST_MYSQL_HOST')
        ONBST_MYSQL_DB = getenv('ONBST_MYSQL_DB')
        ONBST_MYSQL_PORT = getenv('ONBST_MYSQL_PORT')
        ONBST_ENV = getenv('ONBST_ENV')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:{}/{}'
                                      .format(ONBST_MYSQL_USER,
                                              ONBST_MYSQL_PWD,
                                              ONBST_MYSQL_HOST,
                                              ONBST_MYSQL_PORT,
                                              ONBST_MYSQL_DB),
                                      pool_pre_ping=True)
        
        if ONBST_ENV == 'test':
            Base.metadata.drop_all(self.__engine)
        
    def all(self, cls=None):
        """
        Query on the current database session all objects of the given class 
        """
        if cls:
            if cls not in classes.values():
                return {}
            objects = self.__session.query(cls).all()
        else:
            objects = []
            for cls in classes.values():
                objects += self.__session.query(cls).all()
        return {obj.__class__.__name__ + '.' + obj.id: obj for obj in objects}
    
    def new(self, obj):
        """
        Add the object to the current database session
        """
        self.__session.add(obj)
    
    def save(self):
        """
        Commit all changes of the current database session
        """
        self.__session.commit()
    
    def delete(self, obj=None):
        """
        Delete from the current database session obj if not None
        """
        if obj:
            self.__session.delete(obj)
    
    def reload(self):
        """
        Create all tables in the database
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
    
    def close(self):
        """
        Close the current session
        """
        self.__session.close()
    
    def get(self, cls, id):
        """
        Get an object from the current session
        """
        if cls not in classes.values():
            return None
        
        all_cls = models.storage.all(cls)
        for obj in all_cls.values():
            if obj.id == id:
                return obj
        return None
    
    def count(self, cls=None):
        """
        Get the count of all objects in the database
        """
        if cls:
            return len(models.storage.all(cls).values())
        return len(models.storage.all().values())
