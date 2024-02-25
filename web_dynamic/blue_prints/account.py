#!/usr/bin/python3
""" Init file for account module """
from models import storage
from models.user import User
from models.order import Order
from models.order_status import OrderStatus
from models.order_line import OrderLine
from web_dynamic.blue_prints import bookstore_views
from flask import abort, jsonify, make_response, request, render_template,  redirect, url_for, g, session


@bookstore_views.route('/account', methods=['GET'], strict_slashes=False)
def account():
    """ Retrieves a Account object """
    if not g.user:
        return redirect(url_for('bookstore_views.login'))
    
    user = storage.get(User, session['user_id'])
    if user is None:
        return redirect(url_for('bookstore_views.login'))
    orders = []
    for order in user.orders:
        order_data = order.to_dict()
        order_data['orderlines'] = []
        for order_line in order.orderlines:
            order_data['orderlines'].append(order_line.to_dict())
            order_data['orderlines'][-1]['book'] = order_line.book.to_dict()
        orders.append(order_data)
    
    return render_template('account.html',  orders=orders)