#!/usr/bin/python
""" holds class Review"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """Representation of Review """
    __tablename__ = 'reviews'
    book_id = Column(String(60), ForeignKey('books.id'),
                     nullable=False, primary_key=True)
    user_id = Column(String(60), ForeignKey('users.id'),
                     nullable=False, primary_key=True)
    text = Column(String(1024), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes Review"""
        super().__init__(*args, **kwargs)
