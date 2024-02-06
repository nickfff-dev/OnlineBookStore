#!/usr/bin/python3
""" Module for publishers api that
handles RestFul API actions that involve publishers """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.publisher import Publisher
from models import storage


@app_views.route('/publishers', methods=['GET'], strict_slashes=False)
def get_publishers():
    """ Retrieves the list of all Publisher objects """

    publishers = storage.all(Publisher).values()
    publishers = [publisher.to_dict() for publisher in publishers]

    return jsonify(publishers)


@app_views.route('/publishers/<publisher_id>', methods=['GET'],
                 strict_slashes=False)
def get_publisher(publisher_id):
    """ Retrieves a Publisher object """

    publisher = storage.get(Publisher, publisher_id)

    if publisher is None:
        abort(404)
    return jsonify(publisher.to_dict())


@app_views.route('/publishers/<publisher_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_publisher(publisher_id):
    """ Deletes a Publisher object """

    publisher = storage.get(Publisher, publisher_id)

    if publisher is None:
        abort(404)

    storage.delete(publisher)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/publishers', methods=['POST'], strict_slashes=False)
def post_publisher():
    """ Creates a Publisher """
    if not request.get_json():
        abort(400, description='Not a JSON')

    if 'name' not in request.get_json():
        abort(400, description='Missing name')

    data = request.get_json()
    publisher = Publisher(**data)
    publisher.save()
    return make_response(jsonify(publisher.to_dict()), 201)


@app_views.route('/publishers/<publisher_id>', methods=['PUT'],
                 strict_slashes=False)
def put_publisher(publisher_id):
    """ Updates a Publisher """

    publisher = storage.get(Publisher, publisher_id)

    if publisher is None:
        abort(404)

    if not request.get_json():
        abort(400, description='Not a JSON')

    data = request.get_json()
    for key, value in data.items():
        setattr(publisher, key, value)
    publisher.save()
    return make_response(jsonify(publisher.to_dict()), 200)


@app_views.route('/publishers/<publisher_id>/books', methods=['GET'],
                 strict_slashes=False)
def get_publisher_books(publisher_id):
    """ Retrieves the list of all Book objects of a Publisher """

    publisher = storage.get(Publisher, publisher_id)

    if publisher is None:
        abort(404)

    books = publisher.books
    books = [book.to_dict() for book in books]

    return jsonify(books)
