#!/usr/bin/python3
""" Init file for user module """
from models.user import User
from models import storage
from web_dynamic.blue_prints import bookstore_views
from flask import render_template
from flask import request, jsonify, make_response, abort, session, redirect, url_for
from werkzeug.security import  check_password_hash


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
    user = next((user for user in users if user.email == email and check_password_hash(user.password, password)), None)
    if not user:
        abort(404)
    session.clear()
    session['user_id'] = user.id
    return redirect(url_for('bookstore_views.index'))