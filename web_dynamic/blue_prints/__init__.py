#!/usr/bin/python3
""" Init file for auth module """
from flask import Blueprint, session, g
from models import storage
from models.user import User

bookstore_views = Blueprint('bookstore_views', __name__, url_prefix='/bookstore')

@bookstore_views.before_app_request
def load_logged_in_user():
    """ Before request """
    if 'user_id' in session:
        user = storage.get(User, session['user_id'])
        if user:
            g.user = user.to_dict()
            print(g.user, file=sys.stderr)
        else:
            g.user = None
    else:
        g.user = None

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
from web_dynamic.blue_prints.logout import *
