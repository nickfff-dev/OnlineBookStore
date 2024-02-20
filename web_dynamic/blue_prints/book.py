#!/usr/bin/python3
""" Init file for books module """
from models.book import Book
from models import storage
from models.author import Author
from web_dynamic.blue_prints import bookstore_views
from flask import render_template, abort
import sys

@bookstore_views.route('/books/<book_id>', methods=['GET'], strict_slashes=False)
def book(book_id):
    """ Retrieves a Book object """
    book = storage.get(Book, book_id)
    if book is None:
        return abort(404, description="Not found")

    authors = [
        author.to_dict() for author in book.authors
    ]
    publishers = [
        publisher.to_dict() for publisher in book.publishers
    ]
    categories = [
        category.to_dict() for category in book.categories
    ]
    book = book.to_dict()
    book['authors'] = authors
    book['publishers'] = publishers
    book['categories'] = categories
    return render_template('book.html', book=book)
 