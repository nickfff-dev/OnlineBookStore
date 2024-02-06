#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
from datetime import datetime
import models
from os import getenv
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models.
       Added class attributes
    """

    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    setattr(self, key, value)
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
            if kwargs.get("updated_at", None):
                self.updated_at = datetime.strptime(kwargs['updated_at'],
                                                    '%Y-%m-%dT%H:%M:%S.%f')
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs['created_at'],
                                                    '%Y-%m-%dT%H:%M:%S.%f')
            else:
                self.created_at = datetime.utcnow()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = self.__class__.__name__
        return '[{:s}] ({:s}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Creates a dictionary containing all keys/values of the instance"""
        dictionary = self.__dict__.copy()
        dictionary['__class__'] = self.__class__.__name__
        if 'created_at' in dictionary:
            dictionary['created_at'] = dictionary['created_at'].isoformat()
        if 'updated_at' in dictionary:
            dictionary['updated_at'] = dictionary['updated_at'].isoformat()
        if '_sa_instance_state' in dictionary:
            del dictionary['_sa_instance_state']
        return dictionary

    def delete(self):
        """Delete the current instance from the storage"""
        models.storage.delete(self)
