#!/usr/bin/python3
"""Defines Order class
"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from models.order_item import OrderItem


class Status(PyEnum):
    """_summary_

    Args:
        PyEnum (enum.EnumMeta): class to enumerate Status of orders
    """
    PENDING = 'pending'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'


class Order(BaseModel, Base):
    """Defines Order class and its attributes 

    Args:
        BaseModel (class): the base model class
        Base (class): ORM base class
    """
    __tablename__ = "orders"
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    status = Column(Enum(Status), nullable=False)
    order_items = relationship('OrderItem',
                               backref='order',
                               cascade="all, delete, delete-orphan")
