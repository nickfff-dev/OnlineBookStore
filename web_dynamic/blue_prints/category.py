#!/usr/bin/python3
""" Init file for categories module """
from models.category import Category
from models import storage
from web_dynamic.blue_prints import bookstore_views
from flask import render_template



@bookstore_views.route('/categories/<category_id>', methods=['GET'],
                       strict_slashes=False)
def category(category_id):
    """ Retrieves a Category object """
    categorydata = storage.get(Category, category_id)
    category = categorydata.to_dict()
    books = []
    for x in categorydata.books:
        book = x.to_dict()
        books.append(book)
    
    return render_template('category.html', category=category, books=books)