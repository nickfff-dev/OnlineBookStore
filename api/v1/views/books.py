#!/usr/bin/python3
""" Module for books api that
handles RestFul API actions that involve books """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.book import Book
from models.publisher import Publisher
from models.author import Author
from models.category import Category
from models import storage


@app_views.route('/books', methods=['GET'],
                 strict_slashes=False)
def get_books():
    """ Retrieves the list of all Book objects """

    books = storage.all(Book).values()
    books = [book.to_dict() for book in books]

    return jsonify(books)


@app_views.route('/books/<book_id>', methods=['GET'],
                 strict_slashes=False)
def get_book(book_id):
    """ Retrieves a Book object """

    book = storage.get(Book, book_id)

    if book is None:
        abort(404)
    return jsonify(book.to_dict())


@app_views.route('/books/<book_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_book(book_id):
    """ Deletes a Book object """

    book = storage.get(Book, book_id)

    if book is None:
        abort(404)

    storage.delete(book)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/books', methods=['POST'],
                 strict_slashes=False)
def post_book():
    """ Creates a Book """
    if not request.get_json():
        abort(400, description='Not a JSON')

    if 'title' not in request.get_json():
        abort(400, description='Missing title')

    if 'description' not in request.get_json():
        abort(400, description='Missing description')

    if 'image' not in request.get_json():
        abort(400, description='Missing image')

    if 'isbn' not in request.get_json():
        abort(400, description='Missing isbn')

    if 'price' not in request.get_json():
        abort(400, description='Missing price')

    if 'unitsInStock' not in request.get_json():
        abort(400, description='Missing unitsInStock')

    all_books = storage.all(Book).values()
    existing_book = next(
        (book for book in all_books if
         book.isbn == request.get_json()['isbn']),
        None)
    if existing_book is not None:
        existing_book_obj = storage.get(Book, existing_book.id)
        return make_response(jsonify(existing_book_obj.to_dict()), 200)

    data = request.get_json()
    result = create_book(data)

    if result.get('error', None) is not None:
        abort(400, description=result['error'])

    new_book = storage.get(Book, result['id'])
    return make_response(jsonify(new_book.to_dict()), 201)


@app_views.route('/books/<book_id>', methods=['PUT'],
                 strict_slashes=False)
def put_book(book_id):
    """ Updates a Book object """
    if not request.get_json():
        abort(400, description='Not a JSON')

    book = storage.get(Book, book_id)
    if book is None:
        abort(404)

    data = request.get_json()
    ignore = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(book, key, value)
    storage.save()
    return make_response(jsonify(book.to_dict()), 200)


def create_book(data):
    """
    function to create book data from request data
    data contains another key 'publisher' that has keys 'id'
    and optionally 'name'. if 'name' is present,
    we need to create a new publisher
    if 'name' is not present, we need to find the publisher by 'id'
    data also contains another key 'authors'
    that has an array of objects with keys 'id' and optionally 'name'
    we need to iterate through the array and create new authors
    if 'name' is present and store the 'id' in an array
    if 'name' is not present, we need to append the 'id' to the array
    same for categories """

    # we need to create the book first
    number_of_pages = data.get('numberOfPages', None)
    if number_of_pages is not None:
        number_of_pages = int(number_of_pages)
    book_data = {
        'title': data['title'],
        'description': data['description'],
        'image': data['image'],
        'isbn': data['isbn'],
        'price': float(data['price']),
        'unitsInStock': int(data['unitsInStock']),
        'edition': data.get('edition', None),
        'publish_date': data.get('publish_date', None),
        'numberOfPages': number_of_pages,
        'discount': data.get('discount', 0.0)
    }
    new_book = Book(**book_data)
    new_book.save()

    publishers = data.get('publishers', [])
    if len(publishers) == 0:
        return {'error': 'Missing publishers'}

    authors = data.get('authors', [])
    if len(authors) == 0:
        return {'error': 'Missing authors'}

    categories = data.get('categories', [])
    if len(categories) == 0:
        return {'error': 'Missing categories'}

    all_publishers = storage.all(Publisher).values()
    for publisher in publishers:
        if publisher.get('id', None) is not None:
            publisher_to_add_book = storage.get(Publisher, publisher['id'])
            publisher_to_add_book.books.append(new_book)
            storage.save()
        else:
            if publisher.get('name', None) is None:
                continue
            publisher_name = publisher['name']
            existing_publisher = next(
                (pub for pub in all_publishers if pub.name == publisher_name),
                None)
            if existing_publisher is not None:
                publisher_to_add_book = storage.get(Publisher,
                                                    existing_publisher.id)
                publisher_to_add_book.books.append(new_book)
                storage.save()
            else:
                publisher_kw = {'name': publisher_name}
                new_publisher = Publisher(**publisher_kw)
                new_publisher.save()
                new_publisher.books.append(new_book)
                storage.save()

    for author in authors:
        all_authors = storage.all(Author).values()
        if author.get('id', None) is not None:
            author_to_add = storage.get(Author, author['id'])
            author_to_add.books.append(new_book)
            storage.save()
        else:
            if author.get('name', None) is None:
                continue
            existing_author = next(
                (auth for auth in all_authors if
                 auth.fullNames == author['name']),
                None)
            if existing_author is not None:
                author_to_add = storage.get(Author, existing_author.id)
                author_to_add.books.append(new_book)
                storage.save()
            else:
                author_kw = {'fullNames': author['name']}
                new_author = Author(**author_kw)
                new_author.save()
                new_author.books.append(new_book)
                storage.save()

    for category in categories:
        if category.get('id', None) is not None:
            category_to_add = storage.get(Category, category['id'])
            category_to_add.books.append(new_book)
            storage.save()
        else:
            if category.get('name', None) is None:
                continue
            all_categories = storage.all(Category).values()
            existing_category = next(
                (cat for cat in all_categories if
                 cat.name == category['name']),
                None)
            if existing_category is not None:
                category_to_add = storage.get(Category, existing_category.id)
                category_to_add.books.append(new_book)
                storage.save()
            else:
                category_kw = {'name': category['name']}
                new_category = Category(**category_kw)
                new_category.save()
                new_category.books.append(new_book)
                storage.save()

    return {"id": new_book.id}
