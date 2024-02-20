#!/usr/bin/python3
""" Init file for landing page view module """
from models.book import Book
from models.author import Author
from models.category import Category
from models.publisher import Publisher
from models import storage
from web_dynamic.blue_prints import bookstore_views
from flask import render_template
import sys


@bookstore_views.route('/', methods=['GET'], strict_slashes=False)
def index():
    """ Retrieves the list of all Book objects """
    all_books = storage.all(Book).values()
    books = []
    authors = []
    publishers = []
    categories = []
    for item in all_books:
        book = item.to_dict()
        books.append(book)

    all_authors = storage.all(Author).values()
    for author_item in all_authors:
        author = author_item.to_dict()
        authors.append(author)
    
    all_publishers = storage.all(Publisher).values()
    for publisher_item in all_publishers:
        publisher = publisher_item.to_dict()
        publishers.append(publisher)
    
    all_categories = storage.all(Category).values()
    for category_item in all_categories:
        category = category_item.to_dict()
        categories.append(category)
    
    return render_template('index.html', books=books, authors=authors,
                            publishers=publishers, categories=categories)
