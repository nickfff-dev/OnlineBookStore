#!/usr/bin/python3
""" Init file for auth module """
from flask import Blueprint

bookstore_views = Blueprint('bookstore_views', __name__, url_prefix='/bookstore')

from web_dynamic.blue_prints.books import *
from web_dynamic.blue_prints.categories import *
from web_dynamic.blue_prints.publishers import *
from web_dynamic.blue_prints.index import *
from web_dynamic.blue_prints.authors import *
from web_dynamic.blue_prints.publisher import *
from web_dynamic.blue_prints.author import *
from web_dynamic.blue_prints.book import *
from web_dynamic.blue_prints.category import *
from web_dynamic.blue_prints.login import *
from web_dynamic.blue_prints.register import *
from web_dynamic.blue_prints.landing import *
from web_dynamic.blue_prints.about import *
from web_dynamic.blue_prints.account import *
