#!/usr/bin/python3
"""This module defines a class User"""
import models
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = 'users'
    firstName = Column(String(128), nullable=True)
    lastName = Column(String(128), nullable=True)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    zipCode = Column(String(128), nullable=True)
    street = Column(String(128), nullable=True)
    
    def __init__(self, *args, **kwargs):
        """Initializes a user"""
        super().__init__(*args, **kwargs)
