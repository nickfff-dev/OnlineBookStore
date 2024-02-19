#!/usr/bin/python3
""" Init file for authors module """
from models.author import Author
from models import storage
from web_dynamic.blue_prints import bookstore_views
from flask import abort, jsonify, make_response, request, render_template



@bookstore_views.route('/authors/<author_id>', methods=['GET'],
                          strict_slashes=False)
def author(author_id):
    """ Retrieves a Author object """
    authordata = storage.get(Author, author_id)
    if authordata is None:
        abort(404)
    author = authordata.to_dict()
    return render_template('author.html', author=author)