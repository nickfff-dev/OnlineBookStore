#!/usr/bin/python3
""" Init file for publishers module """
from models.publisher import Publisher
from models import storage
from web_dynamic.blue_prints import bookstore_views
from flask import render_template


@bookstore_views.route('/publishers', methods=['GET'], strict_slashes=False)
def publishers():
    """ Retrieves the list of all Publisher objects """

    all_publishers = storage.all(Publisher).values()
    publishers = []
    for item in all_publishers:
        publisher = item.to_dict()
        for x in item.books:
            book = x.to_dict()
            for author in x.authors:
                book['authors'].append(author.to_dict())
            for publisher in x.publishers:
                book['publishers'].append(publisher.to_dict())
            for category in x.categories:
                book['categories'].append(category.to_dict())
            publisher['books'].append(book)
        publishers.append(publisher)

    return render_template('publishers.html', publishers=publishers)