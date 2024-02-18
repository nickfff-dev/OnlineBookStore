#!/usr/bin/python3
"""This module defines a class Book"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship


class Book(BaseModel, Base):
    """This class defines a book by various attributes"""
    __tablename__ = 'books'
    title = Column(String(1024), nullable=False)
    description = Column(String(2024), nullable=True)
    image = Column(String(1024), nullable=True)
    isbn = Column(String(20), unique=True, nullable=False)
    edition = Column(String(126), nullable=True)
    publish_date = Column(String(60), nullable=True)
    numberOfPages = Column(Integer, nullable=True)
    price = Column(Float, nullable=False)
    unitsInStock = Column(Integer, nullable=False)
    discount = Column(Float, nullable=False, default=0.0)
    reviews = relationship('Review', backref='book',
                           cascade='all, delete, delete-orphan')
    orderlines = relationship('OrderLine', backref='book')

    def __init__(self, *args, **kwargs):
        """Initializes a book"""
        super().__init__(*args, **kwargs)
