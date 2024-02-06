#!/usr/bin/python3
"""This module defines a class Category"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship


category_book = Table(
    'category_book',
    Base.metadata,
    Column('category_id', String, ForeignKey('categories.id'),
           primary_key=True),
    Column('book_id', String, ForeignKey('books.id'),
           primary_key=True),
)


class Category(BaseModel, Base):
    """This class defines a category by various attributes"""
    __tablename__ = 'categories'
    name = Column(String(128), nullable=False, unique=True)
    books = relationship('Book', secondary='category_book',
                         backref='categories', viewonly=False)

    def __init__(self, *args, **kwargs):
        """Initializes a category"""
        super().__init__(*args, **kwargs)
