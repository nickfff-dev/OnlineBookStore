#!/usr/bin/python3
"""This module defines a class Book"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship


class Book(BaseModel, Base):
    """This class defines a book by various attributes"""
    __tablename__ = 'books'
    title = Column(String(1024), nullable=False)
    description = Column(String(1024), nullable=True)
    image = Column(String(1024), nullable=True)
    isbn = Column(String(20), Unique=True, nullable=False)
    edition = Column(String(20), nullable=True)
    price = Column(Float, nullable=False)
    unitsInStock = Column(Integer, nullable=False)
    discount = Column(Float, nullable=False, default=0.0)
    publisher_id = Column(String(60), String, ForeignKey('publishers.id'),
                          nullable=False)
    reviews = relationship('Review', backref='book',
                           cascade='all, delete, delete-orphan')

    def __init__(self, *args, **kwargs):
        """Initializes a book"""
        super().__init__(*args, **kwargs)
