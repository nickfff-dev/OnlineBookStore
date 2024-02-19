#!/usr/bin/python3
""" Init file for publishers module """
from models.publisher import Publisher
from models import storage
from web_dynamic.blue_prints import bookstore_views
from flask import render_template


@bookstore_views.route('/publishers/<publisher_id>', methods=['GET'],
                          strict_slashes=False)
def publisher(publisher_id):
    """ Retrieves a Publisher object """
    publisherdata = storage.get(Publisher, publisher_id)
    publisher = publisherdata.to_dict()
    for x in publisherdata.books:
        book = x.to_dict()
        for author in x.authors:
            book['authors'].append(author.to_dict())
        for publisher in x.publishers:
            book['publishers'].append(publisher.to_dict())
        for category in x.categories:
            book['categories'].append(category.to_dict())
        publisher['books'].append(book)
    
    return render_template('publisher.html', publisher=publisher)