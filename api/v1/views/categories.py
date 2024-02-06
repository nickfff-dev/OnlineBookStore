#!/usr/bin/python3
""" Module for categories api that
handles RestFul API actions that involve categories """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.category import Category
from models import storage


@app_views.route('/categories', methods=['GET'],
                 strict_slashes=False)
def get_categories():
    """ Retrieves the list of all Category objects """

    categories = storage.all(Category).values()
    categories = [category.to_dict() for category in categories]

    return jsonify(categories)


@app_views.route('/categories/<category_id>', methods=['GET'],
                 strict_slashes=False)
def get_category(category_id):
    """ Retrieves a Category object """

    category = storage.get(Category, category_id)

    if category is None:
        abort(404)
    return jsonify(category.to_dict())


@app_views.route('/categories/<category_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_category(category_id):
    """ Deletes a Category object """

    category = storage.get(Category, category_id)

    if category is None:
        abort(404)

    storage.delete(category)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/categories', methods=['POST'], strict_slashes=False)
def post_category():
    """ Creates a Category """
    if not request.json:
        abort(400, description='Not a JSON')

    if 'name' not in request.json:
        abort(400, description='Missing name')

    data = request.get_json()
    category = Category(**data)
    category.save()
    return make_response(jsonify(category.to_dict()), 201)


@app_views.route('/categories/<category_id>', methods=['PUT'],
                 strict_slashes=False)
def put_category(category_id):
    """ Updates a Category object """

    category = storage.get(Category, category_id)

    if category is None:
        abort(404)

    if not request.json:
        abort(400, description='Not a JSON')

    data = request.get_json()
    ignore = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(category, key, value)
    storage.save()
    return make_response(jsonify(category.to_dict()), 200)


@app_views.route('/categories/<category_id>/books', methods=['GET'],
                 strict_slashes=False)
def get_category_books(category_id):
    """ Retrieves the list of all Book objects of a Category """

    category = storage.get(Category, category_id)

    if category is None:
        abort(404)

    books = [book.to_dict() for book in category.books]

    return jsonify(books)
