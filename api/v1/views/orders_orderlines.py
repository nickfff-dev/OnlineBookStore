#!/usr/bin/python3
""" Module for users api that
handles RestFul API actions that involve orders and orderlines """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.order import Order
from models.order_line import OrderLine
from models import storage
from models.user import User
from models.book import Book


@app_views.route('/orders/<order_id>/orderlines', methods=['GET'],
                 strict_slashes=False)
def get_orderlines(order_id):
    """ Retrieves the list of all OrderLine objects of an Order """

    order = storage.get(Order, order_id)

    if order is None:
        abort(404)

    orderlines = [orderline.to_dict() for orderline in order.orderlines]

    return jsonify(orderlines)


@app_views.route('/orderlines/<orderline_id>', methods=['GET'],
                 strict_slashes=False)
def get_orderline(orderline_id):
    """ Retrieves a OrderLine object """

    orderline = storage.get(OrderLine, orderline_id)

    if orderline is None:
        abort(404)

    return jsonify(orderline.to_dict())


@app_views.route('/orders/<order_id>/orderlines', methods=['POST'],
                 strict_slashes=False)
def post_orderline(order_id):
    """ Creates a OrderLine """
    if not request.get_json():
        abort(400, description='Not a JSON')

    if 'book_id' not in request.get_json():
        abort(400, description='Missing book_id')

    if 'quantity' not in request.get_json():
        abort(400, description='Missing quantity')

    order = storage.get(Order, order_id)

    if order is None:
        abort(404)

    data = request.get_json()

    book = storage.get(Book, data['book_id'])

    if book is None:
        abort(404)
    # we can calculate the subtotal here for the orderline
    price = book.price
    discount = book.discount if book.discount else 0
    unit_sale_price = price - (price * discount)
    sub_total = unit_sale_price * data['quantity']

    orderline = OrderLine(order_id=order.id, book_id=book.id,
                          quantity=data['quantity'], sub_total=sub_total)
    orderline.save()
    # we need to update the order total
    order.total += sub_total
    order.save()
    return make_response(jsonify(orderline.to_dict()), 201)


@app_views.route('/orderlines/<orderline_id>', methods=['PUT'],
                 strict_slashes=False)
def put_orderline(orderline_id):
    """ Updates a OrderLine """

    orderline = storage.get(OrderLine, orderline_id)

    if orderline is None:
        abort(404)

    if not request.get_json():
        abort(400, description='Not a JSON')

    data = request.get_json()

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'order_id',
                       'book_id']:
            setattr(orderline, key, value)
    orderline.save()

    return make_response(jsonify(orderline.to_dict()), 200)


@app_views.route('/orderlines/<orderline_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_orderline(orderline_id):
    """ Deletes a OrderLine """

    orderline = storage.get(OrderLine, orderline_id)

    if orderline is None:
        abort(404)

    storage.delete(orderline)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/orders/<order_id>/orderlines/<orderline_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_orderline_from_order(order_id, orderline_id):
    """ Deletes a OrderLine from an Order """

    order = storage.get(Order, order_id)

    if order is None:
        abort(404)

    orderline = storage.get(OrderLine, orderline_id)

    if orderline is None:
        abort(404)

    if orderline.order_id != order.id:
        abort(404)

    storage.delete(orderline)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/orders/<order_id>/orderlines/<orderline_id>',
                 methods=['PUT'], strict_slashes=False)
def put_orderline_to_order(order_id, orderline_id):
    """ Updates a OrderLine from an Order """

    order = storage.get(Order, order_id)

    if order is None:
        abort(404)

    orderline = storage.get(OrderLine, orderline_id)

    if orderline is None:
        abort(404)

    if orderline.order_id != order.id:
        abort(404)

    if not request.get_json():
        abort(400, description='Not a JSON')

    data = request.get_json()

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'order_id',
                       'book_id']:
            setattr(orderline, key, value)

    orderline.save()

    return make_response(jsonify(orderline.to_dict()), 200)
