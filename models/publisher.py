#!/usr/bin/python3
"""This module defines a class Publisher"""
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base


class Publisher(BaseModel, Base):
    """This class defines a publisher by various attributes"""
    __tablename__ = 'publishers'
    name = Column(String(128), nullable=False, unique=True)

    def __init__(self, *args, **kwargs):
        """Initializes a user"""
        super().__init__(*args, **kwargs)
