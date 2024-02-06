#!/usr/bin/python3
"""This module defines a class Publisher"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Publisher(BaseModel, Base):
    """This class defines a publisher by various attributes"""
    __tablename__ = 'publishers'
    name = Column(String(128), nullable=False, unique=True)
    books = relationship('Book', backref='publisher',
                         cascade='all, delete, delete-orphan')

    def __init__(self, *args, **kwargs):
        """Initializes a user"""
        super().__init__(*args, **kwargs)
