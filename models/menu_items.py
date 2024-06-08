#!/usr/bin/python3
"""Defines MenuItem class
"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, TEXT, DECIMAL
from sqlalchemy.orm import relationship
from models.order_items import OrderItem
from models.recipes import Recipe
from os import getenv


class MenuItem(BaseModel, Base):
    """Defines MenuItems class and its attributes 

    Args:
        BaseModel (class): the base model class
        Base (class): ORM base class
    """
    if getenv("TYPE_STORAGE") == 'db':
        __tablename__ = "menu_items"

        name = Column(String(128), nullable=False)
        description = Column(TEXT, nullable=True)
        price = Column(DECIMAL(10, 2), nullable=False)
        picture = Column(String(255), nullable=True)
        category = Column(String(255), nullable=False)
        recipes = relationship('Recipe',
                            backref='menu_item',
                            cascade="all, delete, delete-orphan")

        order_items = relationship('OrderItem',
                                backref='menu_item',
                                cascade="all, delete, delete-orphan")
    else:
        name = ""
        description = ""
        price = 0
        picture = ""
        category = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    if getenv("TYPE_STORAGE") == 'db':
        @property
        def order_items(self):

            all_items = []
            all_i = models.storage.all(OrderItem)
            for item in all_i.values():
                if item.id == self.id:
                    all_items.append(item)
            return all_items

    if getenv("TYPE_STORAGE") == 'db':
        @property
        def recipes(self):

            all_items = []
            all_i = models.storage.all(Recipe)
            for item in all_i.values():
                if item.id == self.id:
                    all_items.append(item)
            return all_items
