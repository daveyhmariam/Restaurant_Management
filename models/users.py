#!/usr/bin/python3
"""Defines User class
"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from models.orders import Order


class Role(PyEnum):
    """_summary_

    Args:
        PyEnum (enum.EnumMeta): class to enumerate role of users
    """
    CUSTOMER = 'customer'
    ADMIN = 'admin'
    STAFF = 'staff'


class User(BaseModel, Base):
    """Defines User class and its attributes 

    Args:
        BaseModel (class): the base model class
        Base (class): ORM base class
    """
    __tablename__ = "users"
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    role = Column(Enum(Role), nullable=False)

    orders = relationship('Order',
                          backref='user',
                          cascade="all, delete, delete-orphan")
