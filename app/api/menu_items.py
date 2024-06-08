#!/usr/bin/python3
"""
REST API actions for MenuItem class
"""
from models import storage
from models.menu_items import MenuItem
from app.api import api
from flask import abort, jsonify, make_response, request

@api.route('/menu', methods=['GET'], strict_slashes=False)
def get_menus():
    """
    Retrieve all menu items.
    """
    all_menu = storage.all(MenuItem).values()
    menu_list = [item.to_dict() for item in all_menu]
    return jsonify(menu_list)

@api.route('/menu/<id>', methods=['GET'], strict_slashes=False)
def get_menu(id):
    """
    Retrieve a menu item by ID.

    Args:
        id (str): The ID of the menu item.

    Returns:
        json: JSON representation of the menu item.
    """
    menu = storage.get(MenuItem, id)
    if not menu:
        abort(404)
    return jsonify(menu.to_dict())

@api.route('/menu/<id>', methods=['DELETE'], strict_slashes=False)
def delete_menu(id):
    """
    Delete a menu item by ID.

    Args:
        id (str): The ID of the menu item.

    Returns:
        json: Empty JSON response with status 200.
    """
    menu = storage.get(MenuItem, id)
    if not menu:
        abort(404)
    storage.delete(menu)
    storage.save()
    return make_response(jsonify({}), 200)

@api.route('/menu', methods=['POST'], strict_slashes=False)
def create_menu():
    """
    Create a new menu item.

    Expects JSON request with 'name' and 'price'.

    Returns:
        json: JSON representation of the created menu item with status 201.
    """
    if not request.get_json():
        abort(400, description="NOT A JSON")
    if "name" not in request.get_json():
        abort(400, description="MISSING name")
    if "price" not in request.get_json():
        abort(400, description="MISSING price")

    data = request.get_json()
    new_menu_item = MenuItem(**data)
    new_menu_item.save()
    return make_response(jsonify(new_menu_item.to_dict()), 201)

@api.route('/menu/<id>', methods=['PUT'], strict_slashes=False)
def update_menu(id):
    """
    Update an existing menu item by ID.

    Args:
        id (str): The ID of the menu item.

    Expects JSON request with updated data.

    Returns:
        json: JSON representation of the updated menu item with status 200.
    """
    menu = storage.get(MenuItem, id)
    if not menu:
        abort(404)
    if not request.get_json():
        abort(400, description="NOT JSON")

    data = request.get_json()
    immutable_fields = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in immutable_fields:
            setattr(menu, key, value)
    storage.save()
    return make_response(jsonify(menu.to_dict()), 200)

if __name__ == "__main__":
    api.run()
