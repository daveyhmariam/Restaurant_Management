#!/usr/bin/python3
from models.orders import Order, Status
from models.base_model import Base
from models import storage
from models.users import User
from models.menu_items import MenuItem
from models.order_items import OrderItem
from models.inventory_items import InventoryItem
from models.recipes import Recipe
from sqlalchemy.exc import IntegrityError
import json


if  __name__ == "__main__":

    with open("/home/dave/alx_2/Restaurant_Management/mock_data4.json", 'r') as file:
        data = json.load(file)
        inventory = data["inventory"]

        for inv in inventory:
            try:
                new = InventoryItem(name=inv["name"],
                                    quantity=inv["quantity"],
                                    unit=inv["unit"])
                storage.new(new)
                storage.save()
            except IntegrityError as e:
                storage.rollback()
        all_inv = storage.all(InventoryItem).values()
        dishes = data["menus"]
        for dish in dishes:
            picture = dish["name"]
            picture = picture.replace(" ", "_") + ".jpg"
            new = MenuItem(name=dish["name"],
                            description=dish["description"],
                            price=dish["price"],
                            picture=picture,
                            category=dish["category"])
            res = dish["recipes"]
            for re in res:
                for inv in all_inv:
                    if inv.name == re["ingredient"]:
                        new_res = Recipe(quantity=re["quantity"],
                                         unit=re["unit"],
                                            menu_item_id=new.id,
                                            inventory_item_id=inv.id)
                        storage.new(new_res)
            storage.new(new)
            storage.save()

    '''
    menu = storage.all(MenuItem).values()
    for men in menu:
        men.picture = men.picture.replace(" ", "_") + ".jpg"
    storage.save()
    '''