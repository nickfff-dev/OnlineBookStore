#!/usr/bin/python3
""" Init file for user module """
from models.user import User
from models import storage
from web_dynamic.blue_prints import bookstore_views
from flask import render_template
from flask import request, jsonify, make_response, abort


@bookstore_views.route('/login', methods=['GET','POST'], strict_slashes=False)
def login():
    """ Retrieves the login page """
    if request.method == 'GET':
        return render_template('login.html')

    """ Logs in a user """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        abort(400, 'Not a JSON')
    users = storage.all(User).values()
    user = next((user for user in users if user.email == email and user.password == password), None)
    if not user:
        abort(404)
    return make_response(jsonify(user.to_dict()), 200)