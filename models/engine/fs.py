#!/usr/bin/python3
"""Engine for file storage
"""
from models.base_model import BaseModel
import json


class FileStorage:
    """class for file storage engine that stores objects
        to a file in json format
    """
    __file = "objects.json"
    __objects = {}

    def all(self):
        """
        return dictionary that holds all objects or objects of
        cls if cls is provided
        """
        return type(self).__objects.copy()

    def delete(self, obj=None):
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            if key in type(self).__objects.keys():
                del type(self).__objects[key]

    def new(self, obj):
        """
        add new object to objects dictionary

        Args:
            obj (instance): new object to add
        """
        if obj:
            type(self).__objects["{}.{}".format(type(obj).__name__,
                                 obj.id)] = obj

    def save(self):
        """
        Serializes __objects to the JSON file (path: __file_path)

        """
        try:
            with open(type(self).__file, "w") as file:
                temp = {}
                temp.update(type(self).__objects)
                for key, value in temp.items():
                    temp[key] = value.to_dict()
                json.dump(temp, file, indent=4)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def reload(self):

        classes = {"BaseModel": BaseModel}

        try:
            temp = {}
            with open(type(self).__file, "r") as file:
                temp = json.load(file)
            for key, value in temp.items():
                type(self).__objects[key] = classes[value["__class__"]](**value)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def close(self):
        self.reload()
