#!/usr/bin/python3
"""This module defines a class Publisher"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship


publisher_book = Table(
    'publisher_book',
    Base.metadata,
    Column('publisher_id', String(60), ForeignKey('publishers.id'),
           primary_key=True),
    Column('book_id', String(60), ForeignKey('books.id'), primary_key=True)
)


class Publisher(BaseModel, Base):
    """This class defines a publisher by various attributes"""
    __tablename__ = 'publishers'
    name = Column(String(128), nullable=False, unique=True)
    books = relationship('Book', secondary='publisher_book',
                         backref='publishers', viewonly=False)

    def __init__(self, *args, **kwargs):
        """Initializes a user"""
        super().__init__(*args, **kwargs)
