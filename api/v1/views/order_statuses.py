#!/usr/bin/python3
""" Module for users api that
handles RestFul API actions that involve orders and statuses """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.order import Order
from models.order_status import OrderStatus, OrderStatusType
from models import storage


@app_views.route('/orders/<order_id>/statuses', methods=['GET'],
                 strict_slashes=False)
def get_statuses(order_id):
    """ Retrieves the list of all OrderStatus objects of an Order """

    order = storage.get(Order, order_id)

    if order is None:
        abort(404)

    statuses = [status.to_dict() for status in order.statuses]

    return jsonify(statuses)


@app_views.route('/statuses/<status_id>', methods=['GET'],
                 strict_slashes=False)
def get_status(status_id):
    """ Retrieves a OrderStatus object """

    status = storage.get(OrderStatus, status_id)

    if status is None:
        abort(404)

    return jsonify(status.to_dict())


@app_views.route('/orders/<order_id>/statuses', methods=['POST'],
                 strict_slashes=False)
def post_status(order_id):
    """ Creates a OrderStatus """
    if not request.get_json():
        abort(400, description='Not a JSON')

    if 'status' not in request.get_json():
        abort(400, description='Missing status')

    order = storage.get(Order, order_id)

    if order is None:
        abort(404)

    data = request.get_json()
    new_status_status = None
    # we need to use OrderStatusType to validate the status
    status_names = {"pending": OrderStatusType.pending,
                    "paid": OrderStatusType.paid,
                    "shipped": OrderStatusType.shipped,
                    "delivered": OrderStatusType.delivered,
                    "canceled": OrderStatusType.canceled}
    for item in status_names:
        if data['status'] == item:
            new_status_status = status_names[item]
            break
    new_status = OrderStatus(order_id=order.id,
                             status=new_status_status, is_current=True)
    new_status.save()
    return make_response(jsonify(new_status.to_dict()), 201)


@app_views.route('/statuses/<status_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_status(status_id):
    """ Deletes a OrderStatus object """

    status = storage.get(OrderStatus, status_id)

    if status is None:
        abort(404)

    storage.delete(status)
    storage.save()
    return make_response(jsonify({}), 200)
