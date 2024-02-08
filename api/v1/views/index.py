#!/usr/bin/python3
""" Index module for the api """
from flask import jsonify
from models.author import Author
from models.book import Book
from models.category import Category
from models.order import Order
from models.publisher import Publisher
from models.review import Review
from models.user import User
from models.order_line import OrderLine
from models.order_status import OrderStatus
from models import storage
from api.v1.views import app_views
from sqlalchemy.inspection import inspect


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Retrieves the status of the api """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """ Retrieves the stats of the api """
    classes = [Author, Book, Category, Order, Publisher, Review, User,
               OrderLine, OrderStatus]
    names = ["authors", "books", "categories", "orders", "publishers",
             "reviews", "users", "orderlines", "orderstatuses"]
    stats = {}
    for i in range(len(classes)):
        stats[names[i]] = storage.count(classes[i])
        stats[names[i] + "_relations"] =  \
            inspect(classes[i]).relationships.keys()
    return jsonify(stats)
