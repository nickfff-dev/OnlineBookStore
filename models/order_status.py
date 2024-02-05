#!/usr/bin/python3
"""This module defines a class OrderStatus"""
import models
import enum
from sqlalchemy import Column, String, DateTime, ForeignKey, Computed, Enum, Float, Table, Integer
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship, ForeignKeyConstraint


class OrderStatusType(enum.Enum):
    """This class defines the
    status of an order"""
    pending = 'pending'
    paid = 'paid'
    shipped = 'shipped'
    delivered = 'delivered'
    cancelled = 'cancelled'


class OrderStatus(BaseModel, Base):
    """This class defines a class OrderStatus by various attributes"""
    __tablename__ = 'orderStatus'
    order_id = Column(String(128), ForeignKey('orders.id'), primary_key=True, nullable=False)
    order_date = Column(DateTime, ForeignKey('orders.order_date'), primary_key=True, nullable=False)
    status = Column(Enum(OrderStatusType), nullable=False, default=OrderStatusType.pending)
    order = relationship('Order', backref='status', cascade='all, delete, delete-orphan')

    def __init__(self, *args, **kwargs):
        """Initializes a user"""
        super().__init__(*args, **kwargs)
