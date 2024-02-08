#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship


author_book = Table(
    'author_book',
    Base.metadata,
    Column('author_id', String(60), ForeignKey('authors.id'),
           primary_key=True),
    Column('book_id', String(60), ForeignKey('books.id'), primary_key=True)
)


class Author(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = 'authors'
    fullNames = Column(String(256), nullable=False)
    books = relationship('Book', secondary='author_book',
                         backref='authors', viewonly=False)

    def __init__(self, *args, **kwargs):
        """Initializes a user"""
        super().__init__(*args, **kwargs)
