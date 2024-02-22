#!/usr/bin/python3
""" Init file for landing page module """
from web_dynamic.blue_prints import bookstore_views
from flask import render_template



@bookstore_views.route('/landingpage', methods=['GET'],
                          strict_slashes=False)
def landing():
    """ Renders the landing page """
    
    return render_template('landing.html')