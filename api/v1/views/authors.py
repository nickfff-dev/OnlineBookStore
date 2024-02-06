#!/usr/bin/python3
""" Module for authors api that
handles RestFul API actions that involve authors """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.author import Author
from models import storage


@app_views.route('/authors', methods=['GET'], strict_slashes=False)
def get_authors():
    """ Retrieves the list of all Author objects """

    authors = storage.all(Author).values()
    authors = [author.to_dict() for author in authors]

    return jsonify(authors)


@app_views.route('/authors/<author_id>', methods=['GET'], strict_slashes=False)
def get_author(author_id):
    """ Retrieves a Author object """

    author = storage.get(Author, author_id)

    if author is None:
        abort(404)
    return jsonify(author.to_dict())


@app_views.route('/authors/<author_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_author(author_id):
    """ Deletes a Author object """

    author = storage.get(Author, author_id)

    if author is None:
        abort(404)

    storage.delete(author)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/authors', methods=['POST'], strict_slashes=False)
def post_author():
    """ Creates an Author """
    if not request.json:
        abort(400, description='Not a JSON')

    if 'name' not in request.json:
        abort(400, description='Missing name')

    data = request.get_json()
    author = Author(**data)
    author.save()
    return make_response(jsonify(author.to_dict()), 201)


@app_views.route('/authors/<author_id>', methods=['PUT'], strict_slashes=False)
def put_author(author_id):
    """ Updates a Author object """
    if not request.get_json():
        abort(400, description='Not a JSON')

    author = storage.get(Author, author_id)

    if author is None:
        abort(404)

    data = request.get_json()
    ignore = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(author, key, value)
    storage.save()
    return make_response(jsonify(author.to_dict()), 200)


@app_views.route('/authors/<author_id>/books', methods=['GET'],
                 strict_slashes=False)
def get_author_books(author_id):
    """ Retrieves the list of all Book objects of an Author """

    author = storage.get(Author, author_id)

    if author is None:
        abort(404)

    books = [book.to_dict() for book in author.books]

    return jsonify(books)
