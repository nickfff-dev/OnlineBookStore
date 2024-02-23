#!/usr/bin/python3
""" Init file for account module """
from models import storage
from models.user import User
from web_dynamic.blue_prints import bookstore_views
from flask import abort, jsonify, make_response, request, render_template,  redirect, url_for, g


@bookstore_views.route('/account', methods=['GET'], strict_slashes=False)
def account():
    """ Retrieves a Account object """
    if not g.user:
        return redirect(url_for('bookstore_views.login'))
    
    
    return render_template('account.html')