#!/usr/bin/python3
"""
REST API actions for OrderItem class
"""
from models import storage
from models.order_items import OrderItem 
from app.api import api
from flask import abort, jsonify, make_response, request

@api.route('/order_items', methods=['GET'], strict_slashes=False)
def get_order_items():
    """
    Retrieve all order items.
    """
    all_orderitems = storage.all(OrderItem).values()
    order_item_list = [item.to_dict() for item in all_orderitems]
    return jsonify(order_item_list)

@api.route('/order_items/<id>', methods=['GET'], strict_slashes=False)
def get_order_item(id):
    """
    Retrieve an order item by ID.

    Args:
        id (str): The ID of the order item.

    Returns:
        json: JSON representation of the order item.
    """
    order_item = storage.get(OrderItem, id)
    if not order_item:
        abort(404)
    return jsonify(order_item.to_dict())

@api.route('/order_items/<id>', methods=['DELETE'], strict_slashes=False)
def delete_order_item(id):
    """
    Delete an order item by ID.

    Args:
        id (str): The ID of the order item.

    Returns:
        json: Empty JSON response with status 200.
    """
    order_item = storage.get(OrderItem, id)
    if not order_item:
        abort(404)
    storage.delete(order_item)
    storage.save()
    return make_response(jsonify({}), 200)

@api.route('/order_items', methods=['POST'], strict_slashes=False)
def create_order_item():
    """
    Create a new order item.

    Expects JSON request with 'user_id' and 'menu_item_id'.

    Returns:
        json: JSON representation of the created order item with status 201.
    """
    if not request.get_json():
        abort(400, description="NOT A JSON")
    if "user_id" not in request.get_json():
        abort(400, description="MISSING user_id")
    if "menu_item_id" not in request.get_json():
        abort(400, description="MISSING menu_item_id")

    data = request.get_json()
    new_order_item = OrderItem(**data)
    new_order_item.save()
    return make_response(jsonify(new_order_item.to_dict()), 201)

@api.route('/order_items/<id>', methods=['PUT'], strict_slashes=False)
def update_order_item(id):
    """
    Update an existing order item by ID.

    Args:
        id (str): The ID of the order item.

    Expects JSON request with updated data.

    Returns:
        json: JSON representation of the updated order item with status 200.
    """
    order_item = storage.get(OrderItem, id)
    if not order_item:
        abort(404)
    if not request.get_json():
        abort(400, description="NOT JSON")

    data = request.get_json()
    immutable_fields = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in immutable_fields:
            setattr(order_item, key, value)
    storage.save()
    return make_response(jsonify(order_item.to_dict()), 200)

if __name__ == "__main__":
    api.run()
