#!/usr/bin/python3
""" Init file for logout module """
from web_dynamic.blue_prints import bookstore_views
from flask import session, redirect, url_for


@bookstore_views.route('/logout', methods=['GET'], strict_slashes=False)
def logout():
    """ Logs out a user """
    session.clear()
    return redirect(url_for('bookstore_views.index'))