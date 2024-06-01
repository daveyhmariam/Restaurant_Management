#!/usr/bin/python3
"""Engine for file storage
"""
from models.base_model import BaseModel
import json
from models.users import User
from models.orders import Order
from models.order_item import OrderItem
from models.menu_items import MenuItem
from models.recipes import Recipe
from models.inventory_items import InventoryItem


class FileStorage:
    """class for file storage engine that stores objects
        to a file in json format
    """
    __file = "objects.json"
    __objects = {}

    def all(self, cls=None):
        """
        return dictionary that holds all objects or objects of
        cls if cls is provided
        """
        if cls:
            obj = {}
            all_obj = self.__objects
            for key in list(all_obj):
                key_split = key.split(".")
                cls_name = key_split[0]
                if cls_name == cls.__name__:
                    obj.update({key: all_obj[key]})
            return obj
        return self.__objects.copy()

    def delete(self, obj=None):
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            if key in self.__objects.keys():
                del self.__objects[key]

    def new(self, obj):
        """
        add new object to objects dictionary

        Args:
            obj (instance): new object to add
        """
        if obj:
            self.__objects["{}.{}".format(type(obj).__name__,
                                 obj.id)] = obj

    def save(self):
        """
        Serializes __objects to the JSON file (path: __file_path)

        """
        try:
            with open(self.__file, "w") as file:
                temp = {}
                temp.update(self.__objects)
                for key, value in temp.items():
                    temp[key] = value.to_dict()
                json.dump(temp, file, indent=4)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def reload(self):

        classes = {"BaseModel": BaseModel,
                    'User': User,
                    'Order': Order,
                    'OrderItem': OrderItem,
                    'MenuItem': MenuItem,
                    'Recipe': Recipe,
                    'InventoryItem': InventoryItem
        }

        try:
            temp = {}
            with open(self.__file, "r") as file:
                temp = json.load(file)
            for key, value in temp.items():
                self.__objects[key] = classes[value["__class__"]](**value)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def close(self):
        self.reload()
