#!/usr/bin/python3
""" This Module defines the views for the api
Including a blueprint to register various view methods
"""
from api.v1.views.authors import *
from api.v1.views.books import *
from api.v1.views.book_reviews import *
from api.v1.views.categories import *
from api.v1.views.index import *
from api.v1.views.orders import *
from api.v1.views.publishers import *
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
