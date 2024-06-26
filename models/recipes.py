#!/usr/bin/python3
"""Defines Recipe class
"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from os import getenv


class Recipe(BaseModel, Base):
    """Defines Recipe class and its attributes 

    Args:
        BaseModel (class): the base model class
        Base (class): ORM base class
    """
    if getenv("TYPE_STORAGE") == 'db':

        __tablename__ = "recipes"
        quantity = Column(DECIMAL(10, 2), nullable=False)
        unit = Column(String(60), nullable=False)
        menu_item_id = Column(String(60), ForeignKey("menu_items.id"), nullable=False)
        inventory_item_id = Column(String(60), ForeignKey("inventory_items.id"), nullable=False)
    else:
        quantity = 0
        unit = ""
        menu_item_id = ""
        inventory_item_id = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
