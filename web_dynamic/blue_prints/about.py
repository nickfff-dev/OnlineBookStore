#!/usr/bin/python3
""" Init file for about page module """
from web_dynamic.blue_prints import bookstore_views
from flask import render_template



@bookstore_views.route('/about', methods=['GET'],
                          strict_slashes=False)
def about():
    """ Renders the about page """
    return render_template('about.html')