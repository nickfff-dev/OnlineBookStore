#!/usr/bin/python3
"""This module defines a class OrderStatus"""
import enum
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Boolean
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship


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
    order_id = Column(String(128), ForeignKey('orders.id'),
                      primary_key=True, nullable=False)
    order_date = Column(DateTime, ForeignKey('orders.order_date'),
                        primary_key=True, nullable=False)
    status = Column(Enum(OrderStatusType), nullable=False,
                    default=OrderStatusType.pending, primary_key=True)
    is_current = Column(Boolean, nullable=False, default=True)

    def __init__(self, *args, **kwargs):
        """Initializes a user"""
        super().__init__(*args, **kwargs)
