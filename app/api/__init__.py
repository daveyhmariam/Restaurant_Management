#!/usr/bin/python3
"""
Create blueprint
"""
from flask import Blueprint


api = Blueprint("api", __name__, url_prefix="/api")
from app.api.users import *
from app.api.orders import *
from app.api.menu_items import *
from app.api.order_items import *
from app.api.recipes import *
from app.api.inventory_items import *
