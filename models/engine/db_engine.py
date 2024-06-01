#!/usr/bin/python3
"""
Storage engine for database engine
"""

import os
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.users import User
from models.orders import Order
from models.order_item import OrderItem
from models.menu_items import MenuItem
from models.recipes import Recipe
from models.inventory_items import InventoryItem


class DB_Storage():
    """
    Relational database storag engine class
    """
    __engine = None
    __session = None

    def __init__(self):

        user = os.getenv('MYSQL_USER')
        passwd = os.getenv('MYSQL_PWD')
        db = os.getenv('MYSQL_DB')
        host = os.getenv('MYSQL_HOST')

        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(user,
                                                   passwd,
                                                   host,
                                                   db))

    def all(self, cls=None):
        """Returns objects of a class if cls is presnt
            or all objects of not

        Args:
            cls (Class, optional): class of entity model. Defaults to None.
        """
        all_models = {'User': User, 'Order': Order,
                      'OrderItem': OrderItem, 'MenuItem': MenuItem,
                      'Recipe': Recipe, 'InventoryItem': InventoryItem}
        dic = {}
        for cl in all_models.keys():
            if cls is None or cls is cl or cls is all_models[cl]:
                query = self.__session.query(all_models[cl]).all()
                for elem in query:
                    key = "{}.{}".format(type(elem).__name__,
                                         elem.id)
                    dic[key] = elem
        return (dic)

    def new(self, obj):
        """Add new object to to table

        Args:
            obj (instance object): new object
        """
        self.__session.add(obj)

    def save(self):
        """
        Commit changes to table
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete object

        Args:
            obj (object of a class, optional): object to delete.
                                                Defaults to None.
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Configure and create session
        """
        Base.metadata.create_all(self.__engine)
        session_fact = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_fact)
        self.__session = Session()

    def close(self):
        """
        removes session by calling remove() method on self.__session
        """
        self.__session.remove()
