#!/usr/bin/python3
"""Defines User class
"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from models.orders import Order
from os import getenv
from flask_login import UserMixin


class Role(PyEnum):
    """_summary_

    Args:
        PyEnum (enum.EnumMeta): class to enumerate role of users
    """
    CUSTOMER = 'customer'
    ADMIN = 'admin'
    STAFF = 'staff'


class User(BaseModel, UserMixin, Base):
    """Defines User class and its attributes 

    Args:
        BaseModel (class): the base model class
        Base (class): ORM base class
    """
    if getenv("TYPE_STORAGE") == 'db':
        __tablename__ = "users"
        email = Column(String(128), nullable=False, unique=True)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        role = Column(Enum(Role), nullable=False)

        orders = relationship('Order',
                            backref='user',
                            cascade="all, delete, delete-orphan")
    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''
        role = ''

    def to_dict(self):
        res = super().to_dict()
        if getenv("TYPE_STORAGE") == 'db':
            res.update({'role': self.role.value})
        return res

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    if getenv("TYPE_STORAGE") == 'db':
        @property
        def orders(self):

            all_items = []
            all_i = models.storage.all(Order)
            for item in all_i.values():
                if item.user_id == self.id:
                    all_items.append(item)
            return all_items
