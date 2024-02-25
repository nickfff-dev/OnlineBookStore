#!/usr/bin/python3
""" Init file for order module """
from models.order import Order
from models import storage
from web_dynamic.blue_prints import bookstore_views
from flask import render_template, request, redirect, url_for


@bookstore_views.route('/cart', methods=['GET','POST'], strict_slashes=False)
def cart():
    """ Retrieves the list of all Order objects """
    if request.method == 'GET':
        return render_template('cart.html')

