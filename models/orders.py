#!/usr/bin/python3
"""Defines Order class
"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from models.order_items import OrderItem
from os import getenv

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
    if getenv("TYPE_STORAGE") == 'db':

        __tablename__ = "orders"
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        status = Column(Enum(Status), nullable=False)
        order_items = relationship('OrderItem',
                                backref='order',
                                cascade="all, delete, delete-orphan")
    else:
        user_id = ''
        status = ''

    def to_dict(self):
        res = super().to_dict()
        if getenv("TYPE_STORAGE") == 'db':
            res.update({'status': self.status.value})
        return res

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    if getenv("TYPE_STORAGE") == 'db':
        @property
        def order_items(self):

            all_items = []
            all_i = models.storage.all(OrderItem)
            for item in all_i.values():
                if item.order_id == self.id:
                    all_items.append(item)
            return all_items
