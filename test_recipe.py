#!/usr/bin/python3

from models.recipes import Recipe
from models.base_model import Base
from models import storage


if __name__ == "__main__":

    
    par = [{'quantity': 100,
           'unit': 'Gram',
           'price': 300.5,
           'category': 'Fastfood'
           }
    menu = MenuItem(**par)
    storage.new(menu)
    storage.save()

    
    m = storage.all(MenuItem)
    for el in m.values():
        print("{}: {}".format(el.name, el.description))
