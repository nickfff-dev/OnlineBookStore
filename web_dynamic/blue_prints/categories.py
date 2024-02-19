#!/usr/bin/python3
""" Init file for categories module """
from models.category import Category
from models import storage
from web_dynamic.blue_prints import bookstore_views
from flask import render_template


@bookstore_views.route('/categories', methods=['GET'], strict_slashes=False)
def categories():
    """ Retrieves the list of all Category objects """
    all_categories = storage.all(Category).values()
    category_books = [
        {
           
            'category': category.to_dict(),
            'books': [
                book.to_dict()
                for book in category.books
            ]
        }
        for category in all_categories
    ]

    return render_template('categories.html', categories=category_books)
