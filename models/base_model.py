#!/usr/bin/python3
"""
Defines base class for all entities of
the restaurant management system
"""
import os
import uuid
from datetime import datetime
import models
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, DateTime


if os.getenv("TYPE_STORAGE") == 'db':
    Base = declarative_base()
else:
    Base = object

time = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel:
    """Base Model for all entities
    """
    if os.getenv("TYPE_STORAGE") == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
        updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """
        initializes a new object of BaseModel
        """
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.fromisoformat(kwargs["created_at"])
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.fromisoformat(kwargs["updated_at"])
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at
        models.storage.new(self)

    def to_dict(self):
        """returns a dictionary containing all
            keys/values of __dict__ of the instance
        """
        dictionary = self.__dict__.copy()
        from os import getenv
        if getenv('HBNB_TYPE_STORAGE') != 'db':
            dictionary["__class__"] = str(type(self).__name__)
        if "_sa_instance_state" in dictionary.keys():
            dictionary.pop("_sa_instance_state", None)
        dictionary["created_at"] = self.created_at.isoformat()
        dictionary["updated_at"] = self.updated_at.isoformat()
        return dictionary

    def save(self):
        """
        Updates the instance
        """
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def delete(self):
        """delete object"""
        models.storage.delete(self)

    def __str__(self):
        """
        String representation of instance
        """
        return ("[{}] ({}) {}".format(str(type(self).__name__), self.id,
                                      self.__dict__))



if __name__ == "__main__":
    from models import storage
    from models.users import User
    from models.base_model import BaseModel
    b=BaseModel()
    storage.save()
    User()
    storage.save()
    print(storage.count(User))