#!/usr/bin/python3
"""This module defines a class OrderStatus"""
import enum
from sqlalchemy import Column, String, ForeignKey, Enum, Boolean
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship


class OrderStatusType(enum.Enum):
    """This class defines the
    status of an order"""
    pending = 'pending'
    paid = 'paid'
    shipped = 'shipped'
    delivered = 'delivered'
    cancelled = 'canceled'


class OrderStatus(BaseModel, Base):
    """This class defines a class OrderStatus by various attributes"""
    __tablename__ = 'statuses'
    order_id = Column(String(60), ForeignKey('orders.id'), nullable=False)
    status = Column(Enum(OrderStatusType), nullable=False,
                    default=OrderStatusType.pending)
    is_current = Column(Boolean, nullable=False, default=True)

    def __init__(self, *args, **kwargs):
        """Initializes a user"""
        super().__init__(*args, **kwargs)
