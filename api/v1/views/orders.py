#!/usr/bin/python3
""" Module for orders api that
handles RestFul API actions that involve orders """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.order import Order
from models.order_status import OrderStatus, OrderStatusType
from models import storage


def updateOrderStatus(order, status):
    """ Updates the status of an order """

    # we need to first fetch the current status and set is_current to False
    # then create a new status with is_current set to True
    all_statuses = storage.all(OrderStatus).values()
    order_statuses = [status for status in all_statuses
                      if status.order_id == order.id and
                      status.order_date == order.order_date]
    for item in order_statuses:
        item.is_current = False
        storage.save()

    if status == 'cancelled':
        order_status = OrderStatus(order_id=order.id,
                                   order_date=order.order_date,
                                   status=OrderStatusType.cancelled,
                                   is_current=True)
    if status == 'paid':
        order_status = OrderStatus(order_id=order.id,
                                   order_date=order.order_date,
                                   status=OrderStatusType.paid,
                                   is_current=True)
    if status == 'shipped':
        order_status = OrderStatus(order_id=order.id,
                                   order_date=order.order_date,
                                   status=OrderStatusType.shipped,
                                   is_current=True)
    if status == 'delivered':
        order_status = OrderStatus(order_id=order.id,
                                   order_date=order.order_date,
                                   status=OrderStatusType.delivered,
                                   is_current=True)
    if status == 'pending':
        order_status = OrderStatus(order_id=order.id,
                                   order_date=order.order_date,
                                   status=OrderStatusType.pending,
                                   is_current=True)

    order_status.save()
    return


@app_views.route('/orders', methods=['GET'], strict_slashes=False)
def get_orders():
    """ Retrieves the list of all Order objects """

    orders = storage.all(Order).values()
    orders = [order.to_dict() for order in orders]

    return jsonify(orders)


@app_views.route('/orders/<order_id>', methods=['GET'], strict_slashes=False)
def get_order(order_id):
    """ Retrieves a Order object """

    order = storage.get(Order, order_id)

    if order is None:
        abort(404)
    return jsonify(order.to_dict())


@app_views.route('/orders/<order_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_order(order_id):
    """ Deletes a Order object """

    order = storage.get(Order, order_id)

    if order is None:
        abort(404)

    storage.delete(order)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/orders', methods=['POST'], strict_slashes=False)
def post_order():
    """ Creates a Order"""
    if not request.get_json():
        abort(400, description='Not a JSON')

    if 'user_id' not in request.get_json():
        abort(400, description='Missing user_id')

    if 'order_date' not in request.get_json():
        abort(400, description='Missing order_date')

    data = request.get_json()
    order = Order(**data)
    order.save()

    #  we need to create a new orderStatus object
    order_status = OrderStatus(order_id=order.id,
                               order_date=order.order_date,
                               status=OrderStatusType.pending,
                               is_current=True)
    order_status.save()

    return make_response(jsonify(order.to_dict()), 201)


@app_views.route('/orders/<order_id>', methods=['PUT'],
                 strict_slashes=False)
def put_order(order_id):
    """ Updates a Order object """

    order = storage.get(Order, order_id)

    if order is None:
        abort(404)

    if not request.get_json():
        abort(400, description='Not a JSON')

    data = request.get_json()

    ignore = ['id', 'user_id', 'order_date']
    for key, value in data.items():
        if key not in ignore:
            if key == 'status':
                updateOrderStatus(order, value)
            else:
                setattr(order, key, value)

    storage.save()
    return make_response(jsonify(order.to_dict()), 200)
