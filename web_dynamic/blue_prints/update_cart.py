#!/usr/bin/python3
""" Init file for deleting an orderline """
from models import storage
from models.book import Book
from web_dynamic.blue_prints import bookstore_views
from flask import jsonify, request, g, make_response, session, render_template, redirect


@bookstore_views.route('/update_cart/<book_id>', methods=['GET','POST'], strict_slashes=False)
def update_cart(book_id):
    """ takes book_id and removes it from g.cart """
    if request.method == 'GET':
        if session.get('orderlines', None) is not None:
            if book_id in session['orderlines']:
                session['orderlines'].pop(book_id, None)
                g.cart = session['orderlines']
                session.modified = True
                g.cart = session['orderlines']
                return redirect('/bookstore/cart')
    
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

        session['orderlines'][book_id] = order_line[book_id]
        g.cart = session['orderlines']
        session.modified = True
        return redirect('/bookstore/cart')

