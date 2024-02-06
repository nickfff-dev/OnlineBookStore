#!/usr/bin/python3
""" Module for users api that
handles RestFul API actions that involve users """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ Retrieves the list of all User objects """

    users = storage.all(User).values()
    users = [user.to_dict() for user in users]

    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ Retrieves a User object """

    user = storage.get(User, user_id)

    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User object """

    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """ Creates a User """
    if not request.get_json():
        abort(400, description='Not a JSON')

    props = ['email', 'password', 'firstName', 'lastName']
    for prop in props:
        if prop not in request.get_json():
            abort(400, description='Missing ' + prop)

    data = request.get_json()
    user = User(**data)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """ Updates a User object """

    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    if not request.get_json():
        abort(400, description='Not a JSON')

    data = request.get_json()
    for key, value in data.items():
        setattr(user, key, value)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
