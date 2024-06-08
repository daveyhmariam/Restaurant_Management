#!/usr/bin/python3
"""Defines OrderItem class
"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from os import getenv


class OrderItem(BaseModel, Base):
    """Defines OrderItem class and its attributes 

    Args:
        BaseModel (class): the base model class
        Base (class): ORM base class
    """
    if getenv("TYPE_STORAGE") == 'db':
        __tablename__ = "order_items"
        order_id = Column(String(60), ForeignKey("orders.id"), nullable=False)
        menu_item_id = Column(String(60), ForeignKey("menu_items.id"), nullable=False)
    else:
        order_id = ""
        menu_item_id = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
