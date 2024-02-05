#!/usr/bin/python3
"""This module defines a class Order"""
import models
import enum
from sqlalchemy import Column, String, DateTime, ForeignKey, Computed, Float, Table, Integer
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship, ForeignKeyConstraint

orderLine = Table('orderLine', Base.metadata,
    Column('order_id', String, ForeignKey('orders.id'), primary_key=True, nullable=False),
    Column('order_date', DateTime, ForeignKey('orders.order_date'), primary_key=True, nullable=False),
    Column('book_id', String, ForeignKey('books.id'), primary_key=True, nullable=False),
    Column('quantity', Integer, nullable=False),
    Column('unit_sale_price', Float, Computed('SELECT price - (price * discount) FROM books WHERE id = book_id')),
    Column('sub_total', Float, nullable=False, Computed('quantity * unit_sale_price')),
)
query = 'SELECT SUM(sub_total) FROM orderLine WHERE order_id = id AND order_date = order_date'

class Order(BaseModel, Base):
    """This class defines a class Order by various attributes"""
    __tablename__ = 'orders'
    order_date = Column(DateTime, primary_key=True, nullable=False)
    total = Column(Float, nullable=False, Computed(query))
    user_id = Column(String(128), ForeignKey('users.id'), primary_key=True, nullable=False)
    user = relationship('User', backref='orders', cascade='all, delete, delete-orphan')
    books = relationship('Book', secondary='orderLine', backref='orders', viewonly=False)
    
    def __init__(self, *args, **kwargs):
        """Initializes a user"""
        super().__init__(*args, **kwargs)