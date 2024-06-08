#!/usr/bin/python3
from flask import Blueprint


site = Blueprint("site", __name__)

from app.site.site_app import *