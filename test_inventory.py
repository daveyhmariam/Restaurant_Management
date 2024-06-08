#!/usr/bin/python3

from models.inventory_items import InventoryItem
from models.base_model import Base
from models import storage


if __name__ == "__main__":

    
    '''
    par = [{'name': 'cheese',
            'quantity': 10,
            'unit': 'KG'},
           {'name': 'beef',
            'quantity': 35,
            'unit': 'KG'               
           }]

    for p in par:
        inv = InventoryItem(**p)
        storage.new(inv)
        storage.save()
    ''' 

    inv = storage.all(InventoryItem)
    for i in inv.values():
        print(i.name)
