#!/usr/bin/python3
"""This module defines a class OrderLine"""
from models.base_model import BaseModel, Base
from sqlalchemy import (Column, String, ForeignKey, Float, Integer)


class OrderLine(BaseModel, Base):
    """This class defines a class OrderLine by various attributes"""
    __tablename__ = 'orderlines'
    book_id = Column(String(60),  ForeignKey('books.id'), nullable=False)
    order_id = Column(String(60), ForeignKey('orders.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    sub_total = Column(Float, nullable=False)
    unit_sale_price = Column(Float, nullable=False)

    def __init__(self, *args, **kwargs):
        """Initializes a user"""
        super().__init__(*args, **kwargs)
