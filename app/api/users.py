#!/usr/bin/python3
"""
REST api actions for User class
"""
from models import storage
from models.users import User
from app.api import api
from flask import abort, jsonify, make_response, request




@api.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieve all users
    """
    all_users = storage.all(User).values()
    listu = [user.to_dict() for user in all_users]
    return jsonify(listu)

@api.route('/users/<id>', methods=['GET'], strict_slashes=False)
def get_user(id):
    """
    Retrieve a user by ID

    Args:
        id (str): User ID

    Returns:
        json: JSON representation of the user
    """
    user = storage.get(User, id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())

@api.route('/users/<id>', methods=['DELETE'], strict_slashes=False)
def delete_user(id):
    """
    Delete a user by ID

    Args:
        id (str): User ID

    Returns:
        json: Empty JSON response with status 200
    """
    user = storage.get(User, id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)

@api.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Create a new user

    Returns:
        json: JSON representation of the created user
    """
    if not request.get_json():
        abort(400, description="NOT A JSON")
    data = request.get_json()
    if "email" not in data:
        abort(400, description="MISSING email")
    if "password" not in data:
        abort(400, description="MISSING password")

    obj = User(**data)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)

@api.route('/users/<id>', methods=['PUT'], strict_slashes=False)
def update_user(id):
    """
    Update a user by ID

    Args:
        id (str): User ID

    Returns:
        json: JSON representation of the updated user
    """
    user = storage.get(User, id)
    if not user:
        abort(404)

    if not request.get_json():
        abort(400, description="NOT JSON")
    data = request.get_json()
    leave = ['id', 'created_at', 'updated_at', 'email']
    for k, v in data.items():
        if k not in leave:
            setattr(user, k, v)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)


