#!/usr/bin/python3
"""Defines InventoryItem class
"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, TEXT, DECIMAL
from sqlalchemy.orm import relationship
from models.recipes import Recipe


class InventoryItem(BaseModel, Base):
    """Defines InventoryItem class and its attributes 

    Args:
        BaseModel (class): the base model class
        Base (class): ORM base class
    """
    __tablename__ = "inventory_items"

    name = Column(String(128), nullable=False, unique=True)
    quantity = Column(DECIMAL(10, 2), nullable=False)
    unit = Column(String(60), nullable=False)
    recipes = relationship('Recipe',
                           backref='inventory_item',
                           cascade="all, delete, delete-orphan")
