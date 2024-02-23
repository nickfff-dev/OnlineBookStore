#!/usr/bin/python3
""" Init file for user module """
from models.user import User
from models import storage
from web_dynamic.blue_prints import bookstore_views
from flask import render_template
from flask import request, jsonify, make_response, abort, redirect, url_for
from werkzeug.security import generate_password_hash
import sys



@bookstore_views.route('/register', methods=['GET','POST'], strict_slashes=False)
def register():
    """ Retrieves the register page """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        zipCode = request.form.get('zipCode')
        street = request.form.get('street')
        if not email or not password or not firstName or not lastName:
            abort(400, 'Missing parameters')
        data = {
            'email': email,
            'password': generate_password_hash(password, method='scrypt', salt_length=8),
            'firstName': firstName,
            'lastName': lastName,
            'zipCode': zipCode,
            'street': street
        }
        user = User(**data)
        user.save()
        print(user.email, user.password,  file=sys.stderr)
        return redirect(url_for('bookstore_views.login'))
    
    return render_template('register.html')
