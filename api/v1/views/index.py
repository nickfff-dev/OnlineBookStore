#!/usr/bin/python3
""" Index module for the api """
from api.v1.views import app_views
from flask import jsonify
from models.author import Author
from models.book import Book
from models.category import Category
from models.order import Order
from models.order_status import OrderStatus
from models.order_status import OrderStatusType
from models.publisher import Publisher
from models.review import Review
from models.user import User
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Retrieves the status of the api """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """ Retrieves the stats of the api """
    stats = {
        "authors": storage.count(Author),
        "books": storage.count(Book),
        "categories": storage.count(Category),
        "orders": storage.count(Order),
        "publishers": storage.count(Publisher),
        "reviews": storage.count(Review),
        "users": storage.count(User)
    }
    return jsonify(stats)
