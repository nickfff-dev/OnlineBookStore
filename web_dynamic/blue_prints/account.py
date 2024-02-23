#!/usr/bin/python3
""" Init file for account module """
from web_dynamic.blue_prints import bookstore_views
from flask import abort, jsonify, make_response, request, render_template


@bookstore_views.route('/account', methods=['GET'], strict_slashes=False)
def account():
    """ Retrieves a Account object """
    return render_template('account.html')