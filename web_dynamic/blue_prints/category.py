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
        authors = []
        publishers = []
        for author in x.authors:
            authors.append(author.to_dict())
        for publisher in x.publishers:
            publishers.append(publisher.to_dict())
        book['authors'] = authors
        book['publishers'] = publishers
        books.append(book)
    category['books'] = books
    
    return render_template('category.html', category=category)