#!/usr/bin/python3
"""
REST api actions for InventoryItem class
"""
from models import storage
from models.inventory_items import InventoryItem
from app.api import api
from flask import abort, jsonify, make_response, request


@api.route('/inventories', methods=['GET'], strict_slashes=False)

def get_inventories():
    """
    all Inventories
    """
    all_inventories = storage.all(InventoryItem).values()
    listu = []
    for inventory in all_inventories:
        listu.append(inventory.to_dict())
    return jsonify(listu)

@api.route('/inventories/<id>', methods=['GET'], strict_slashes=False)
def get_inventory(id):
    """
    Get inventory based on id

    Args:
        id (str): obj id

    Returns:
        json: json rep of object
    """
    inventories = storage.get(InventoryItem, id)
    if not inventories:
        abort(404)
    return jsonify(inventories.to_dict())

@api.route('/inventories/<id>', methods=['DELETE'], strict_slashes=False)
def delete_inventory(id):
    """
    Delete inventories

    Args:
        id (str): inventory id

    Returns:
        json:
    """
    inventory = storage.get(InventoryItem, id)
    if not inventory:
        abort(404)
    storage.delete(inventory)
    storage.save()

    return make_response(jsonify({}), 200)

@api.route('/inventories', methods=['POST'], strict_slashes=False)
def create_inventory():
    """
    CREATE inventory object
    """
    if not request.get_json():
        abort(400, description="NOT A JSON")
    if "name" not in request.get_json():
        abort(400, description="MISSING name")
    if "quantity" not in request.get_json():
        abort(400, description="MISSING quantity")
    if "unit" not in request.get_json():
        abort(400, description="MISSING unit")
    data = request.get_json()
    obj = InventoryItem(**data)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)

@api.route('/inventories/<id>', methods=['PUT'], strict_slashes=False)
def update_inventory(id):
    """
    Update inventories

    Args:
        id (str): obj id
    """

    inventory = storage.get(InventoryItem, id)

    if not inventory:
        abort(404)

    if not request.get_json():
        abort(400, description="NOT JSON")
    data = request.get_json()
    leave = ['id', 'created_at', 'updated_at']
    for k, v in data.items():
        if k not in leave:
            setattr(inventory, k, v)
    storage.save()
    return make_response(jsonify(inventory.to_dict()), 200)

if __name__ == "__main__":

    api.run()
