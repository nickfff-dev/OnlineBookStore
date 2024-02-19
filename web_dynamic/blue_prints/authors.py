#!/usr/bin/python3
""" Init file for authors module """
from models.author import Author
from models import storage
from web_dynamic.blue_prints import bookstore_views
from flask import abort, jsonify, make_response, request, render_template


@bookstore_views.route('/authors', methods=['GET'], strict_slashes=False)
def authors():
    """ Retrieves the list of all Author objects """

    authors = storage.all(Author).values()
    authors = [author.to_dict() for author in authors]

    return render_template('authors.html', authors=authors)
