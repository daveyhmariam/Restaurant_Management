#!/usr/bin/python3

from models.users import User
from models.base_model import Base
from models import storage
from models.users import Role
from sqlalchemy.exc import IntegrityError


if __name__ == "__main__":
    try:
        par = {'email': "daveyhm@gmail.com",
            'password': "pass",
            'role': Role.CUSTOMER}
        user = User(**par)
        storage.new(user)
        storage.save()
    except IntegrityError as e:
        storage._DB_Storage__session.rollback()
    u = storage.all(User)
    for e in u.values():
        print(e.role.value)
