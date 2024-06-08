#!/usr/bin/python3

from models.orders import Order, Status
from models.base_model import Base
from models import storage
from models.users import User

if __name__ == "__main__":

    '''
    par = {'user_id': '169232fa-0503-4e65-942d-34c661c586d7',
           'status': Status.COMPLETED
           }
    order = Order(**par)
    storage.new(order)
    storage.save
    ()'''
    o = storage.all(Order)
    o = storage.all(Order)
    ur = storage.all(User)
    for e in o.values():
        print(e.user.email)
    for u in ur.values():
        print(u.first_name)
        for od in u.orders:
            print(od.status.value)
