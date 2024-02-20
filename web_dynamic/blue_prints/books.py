#!/usr/bin/python3
""" Init file for books module """
from models.book import Book
from models import storage
from web_dynamic.blue_prints import bookstore_views
from flask import render_template, abort


@bookstore_views.route('/books', methods=['GET'], strict_slashes=False)
def books():
    """ Retrieves the list of all Book objects """
  
    all_books = storage.all(Book).values()
    books = []
    for book in all_books:
        bookdata = book.to_dict()
        for author in book.authors:
            bookdata['authors'].append(author.to_dict())
        books.append(bookdata)
        for publisher in book.publishers:
            bookdata['publishers'].append(publisher.to_dict())
        books.append(bookdata)
        for category in book.categories:
            bookdata['categories'].append(category.to_dict())
        books.append(bookdata)

    return render_template('books.html', books=books)