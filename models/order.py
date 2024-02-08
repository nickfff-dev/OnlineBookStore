#!/usr/bin/python3
"""This module defines a class Order"""
from models.base_model import BaseModel, Base
from sqlalchemy import (Column, String, DateTime, ForeignKey,
                        Float, Table)
from sqlalchemy.orm import relationship

order_orderline = Table(
    'order_orderline',
    Base.metadata,
    Column('order_id', String(60), ForeignKey('orders.id'),
           primary_key=True, nullable=False),
    Column('orderline_id', String(60), ForeignKey('orderlines.id'),
           primary_key=True, nullable=False)
)

order_orderstatus = Table(
    'order_orderstatus',
    Base.metadata,
    Column('order_id', String(60), ForeignKey('orders.id'),
           primary_key=True, nullable=False),
    Column('orderstatus_id', String(60), ForeignKey('statuses.id'),
           primary_key=True, nullable=False)
)


class Order(BaseModel, Base):
    """This class defines a class Order by various attributes"""
    __tablename__ = 'orders'
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    order_date = Column(DateTime, nullable=False)
    total = Column(Float,  nullable=False)
    orderlines = relationship('OrderLine', backref='order',
                              secondary=order_orderline, viewonly=False)
    statuses = relationship('OrderStatus', backref='order',
                            secondary=order_orderstatus, viewonly=False)

    def __init__(self, *args, **kwargs):
        """Initializes a user"""
        super().__init__(*args, **kwargs)
