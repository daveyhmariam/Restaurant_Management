#!/usr/bin/python3
"""
REST api actions for Recipe class
"""
from models import storage
from models.recipes import Recipe
from app.api import api
from flask import abort, jsonify, make_response, request

@api.route('/recipes', methods=['GET'], strict_slashes=False)
def get_recipes():
    """
    Retrieve all recipes.
    """
    all_recipes = storage.all(Recipe).values()
    recipe_list = [recipe.to_dict() for recipe in all_recipes]
    return jsonify(recipe_list)

@api.route('/recipes/<id>', methods=['GET'], strict_slashes=False)
def get_recipe(id):
    """
    Retrieve a recipe by ID.

    Args:
        id (str): The ID of the recipe.

    Returns:
        json: JSON representation of the recipe.
    """
    recipe = storage.get(Recipe, id)
    if not recipe:
        abort(404)
    return jsonify(recipe.to_dict())

@api.route('/recipes/<id>', methods=['DELETE'], strict_slashes=False)
def delete_recipe(id):
    """
    Delete a recipe by ID.

    Args:
        id (str): The ID of the recipe.

    Returns:
        json: Empty JSON response with status 200.
    """
    recipe = storage.get(Recipe, id)
    if not recipe:
        abort(404)
    storage.delete(recipe)
    storage.save()
    return make_response(jsonify({}), 200)

@api.route('/recipes', methods=['POST'], strict_slashes=False)
def create_recipe():
    """
    Create a new recipe.

    Expects JSON request with 'menu_item_id', 'quantity', 'inventory_item_id', and 'unit'.

    Returns:
        json: JSON representation of the created recipe with status 201.
    """
    if not request.get_json():
        abort(400, description="NOT A JSON")
    required_fields = ["menu_item_id", "quantity", "inventory_item_id", "unit"]
    for field in required_fields:
        if field not in request.get_json():
            abort(400, description=f"MISSING {field}")

    data = request.get_json()
    new_recipe = Recipe(**data)
    new_recipe.save()
    return make_response(jsonify(new_recipe.to_dict()), 201)

@api.route('/recipes/<id>', methods=['PUT'], strict_slashes=False)
def update_recipe(id):
    """
    Update an existing recipe by ID.

    Args:
        id (str): The ID of the recipe.

    Expects JSON request with updated data.

    Returns:
        json: JSON representation of the updated recipe with status 200.
    """
    recipe = storage.get(Recipe, id)
    if not recipe:
        abort(404)
    if not request.get_json():
        abort(400, description="NOT JSON")

    data = request.get_json()
    immutable_fields = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in immutable_fields:
            setattr(recipe, key, value)
    storage.save()
    return make_response(jsonify(recipe.to_dict()), 200)

if __name__ == "__main__":
    api.run()
