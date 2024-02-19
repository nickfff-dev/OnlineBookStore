#!/usr/bin/python3
""" Init file for books module """
from models.book import Book
from models import storage
from web_dynamic.blue_prints import bookstore_views
from flask import render_template, abort


@bookstore_views.route('/books', methods=['GET'], strict_slashes=False)
def get_books():
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


@bookstore_views.route('/books/<book_id>', methods=['GET'], strict_slashes=False)
def get_book(book_id):
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
 