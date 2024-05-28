#!/usr/bin/python3
"""
Defines bas class for all entities of
the restaurant management system
"""
import uuid
from datetime import datetime
import models


class BaseModel:

    def __init__(self, *args, **kwargs):
        """
        initializes a new object
        """
        if kwargs:
            del kwargs["__class__"]
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    setattr(self, key, datetime.fromisoformat(value))
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        models.storage.new(self)

    def to_dict(self):
        """returns a dictionary containing all
            keys/values of __dict__ of the instance
        """
        dictionary = self.__dict__.copy()
        dictionary["__class__"] = str(type(self).__name__)
        dictionary["created_at"] = self.created_at.isoformat()
        dictionary["updated_at"] = self.updated_at.isoformat()
        return dictionary

    def save(self):
        """
        Updates the instance
        """
        self.updated_at = datetime.utcnow()
        models.storage.save()


    def __str__(self):
        """
        String representation of instance
        """
        return ("[{}] ({}) ".format(str(type(self).__name__)))

if __name__ == "__main__":
    b=BaseModel()
    models.storage.save()
