#!/usr/bin/python3
""" Init file for orderline module """
from models import storage
from web_dynamic.blue_prints import bookstore_views
from flask import jsonify, request, g, make_response, session, redirect
from models.book import Book
import sys

@bookstore_views.route('/orderline', methods=['POST'], strict_slashes=False)
def orderline():
    """ takes quantity and book_id and adds it to g.cart to be used later to create an order """
    if request.method == 'POST':
        book_id = request.form.get('book_id')
        quantity = request.form.get('quantity')
        unitSalePrice = float(request.form.get('unitSalePrice'))
        
        book = storage.get(Book, book_id)
        order_line = {
        book_id:
            {
            'quantity': int(quantity),
            'unitSalePrice': float(unitSalePrice),
            'title': book.title,
            'edition': book.edition,
            'isbn': book.isbn,
            'image': book.image,
            'sub-total': float(unitSalePrice) * int(quantity)
            }
        }

        if session.get('orderlines', None) is None:
            session['orderlines'] = {}
        session['orderlines'].update(order_line)
        g.cart = session['orderlines']
        session.modified = True
        return f'<sup id="cartlength" class="font-bold">{str(len(g.cart))}</sup>'