#!/usr/bin/python3
"""Defines MenuItem class
"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, TEXT, DECIMAL
from sqlalchemy.orm import relationship
from models.order_item import OrderItem
from models.recipes import Recipe


class MenuItem(BaseModel, Base):
    """Defines MenuItems class and its attributes 

    Args:
        BaseModel (class): the base model class
        Base (class): ORM base class
    """
    __tablename__ = "menu_items"

    name = Column(String(128), nullable=False)
    description = Column(TEXT, nullable=True)
    price = Column(DECIMAL(10, 2), nullable=False)
    picture = Column(String(255), nullable=True)
    category = Column(TEXT)
    recipes = relationship('Recipe',
                           backref='menu_item',
                           cascade="all, delete, delete-orphan")

    order_items = relationship('OrderItem',
                               backref='menu_item',
                               cascade="all, delete, delete-orphan")