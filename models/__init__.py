#!/usr/bin/python3
""""
Initiates th storage engine based on the storage type variable
TYPE_STORAGE
"""
from os import getenv

if getenv('TYPE_STORAGE') == 'db':
    from models.engine.db_engine import DB_Storage
    storage = DB_Storage()
    storage.reload()
else:
    from models.engine.fs import FileStorage
    storage = FileStorage()
    storage.reload()
