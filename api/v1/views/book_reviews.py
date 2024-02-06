#!/usr/bin/python3
""" Module for users api that
handles RestFul API actions that involve reviews """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.book import Book
from models import storage
from models.review import Review
from models.user import User


@app_views.route('/books/<book_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(book_id):
    """ Retrieves the list of all Review objects of a Book """

    book = storage.get(Book, book_id)

    if book is None:
        abort(404)

    reviews = [review.to_dict() for review in book.reviews]

    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(book_id, review_id):
    """ Retrieves a Review object """

    book = storage.get(Book, book_id)

    if book is None:
        abort(404)

    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/books/<book_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(book_id):
    """ Creates a Review """
    if not request.get_json():
        abort(400, description='Not a JSON')

    if 'user_id' not in request.get_json():
        abort(400, description='Missing user_id')

    if 'text' not in request.get_json():
        abort(400, description='Missing content')

    user = storage.get(User, request.get_json()['user_id'])

    if user is None:
        abort(404)

    book = storage.get(Book, book_id)

    if book is None:
        abort(404)

    data = request.get_json()
    data['book_id'] = book_id
    review = Review(**data)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """ Updates a Review object """

    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    if not request.get_json():
        abort(400, description='Not a JSON')

    data = request.get_json()
    ignore = ['id', 'user_id', 'book_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a Review object """

    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)
