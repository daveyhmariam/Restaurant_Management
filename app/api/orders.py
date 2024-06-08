#!/usr/bin/python3
"""
REST API actions for Order class
"""
from models import storage
from models.orders import Order
from app.api import api
from flask import abort, jsonify, make_response, request

@api.route('/orders', methods=['GET'], strict_slashes=False)
def get_orders():
    """
    Retrieve all orders.
    """
    all_orders = storage.all(Order).values()
    order_list = [order.to_dict() for order in all_orders]
    return jsonify(order_list)

@api.route('/orders/<id>', methods=['GET'], strict_slashes=False)
def get_order(id):
    """
    Retrieve an order by ID.

    Args:
        id (str): The ID of the order.

    Returns:
        json: JSON representation of the order.
    """
    order = storage.get(Order, id)
    if not order:
        abort(404)
    return jsonify(order.to_dict())

@api.route('/orders/<id>', methods=['DELETE'], strict_slashes=False)
def delete_order(id):
    """
    Delete an order by ID.

    Args:
        id (str): The ID of the order.

    Returns:
        json: Empty JSON response with status 200.
    """
    order = storage.get(Order, id)
    if not order:
        abort(404)
    storage.delete(order)
    storage.save()
    return make_response(jsonify({}), 200)

@api.route('/orders', methods=['POST'], strict_slashes=False)
def create_order():
    """
    Create a new order.

    Expects JSON request with 'user_id' and 'status'.

    Returns:
        json: JSON representation of the created order with status 201.
    """
    if not request.get_json():
        abort(400, description="NOT A JSON")
    if "user_id" not in request.get_json():
        abort(400, description="MISSING user_id")
    if "status" not in request.get_json():
        abort(400, description="MISSING status")

    data = request.get_json()
    new_order = Order(**data)
    new_order.save()
    return make_response(jsonify(new_order.to_dict()), 201)

@api.route('/orders/<id>', methods=['PUT'], strict_slashes=False)
def update_order(id):
    """
    Update an existing order by ID.

    Args:
        id (str): The ID of the order.

    Expects JSON request with updated data.

    Returns:
        json: JSON representation of the updated order with status 200.
    """
    order = storage.get(Order, id)
    if not order:
        abort(404)
    if not request.get_json():
        abort(400, description="NOT JSON")

    data = request.get_json()
    immutable_fields = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in immutable_fields:
            setattr(order, key, value)
    storage.save()
    return make_response(jsonify(order.to_dict()), 200)

if __name__ == "__main__":
    api.run()
