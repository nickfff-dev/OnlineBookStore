#!/usr/bin/python3
""" Init file for books module """
from models.book import Book
from models import storage
from web_dynamic.blue_prints import bookstore_views
from flask import render_template, abort


@bookstore_views.route('/books/<book_id>', methods=['GET'], strict_slashes=False)
def book(book_id):
    """ Retrieves a Book object """
    book = storage.get(Book, book_id)
    

    if book is None:
        return abort(404, description="Not found")

    authors = []
    publishers = []
    categories = []
    book_obj = book.to_dict()
    # for author in book.authors:
    #     authors.append(author.to_dict())
    # book_obj.update({'authors': authors})


    return render_template('book.html', book=book_obj)
 