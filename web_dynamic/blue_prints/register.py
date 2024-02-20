#!/usr/bin/python3
""" Init file for user module """
from models.user import User
from models import storage
from web_dynamic.blue_prints import bookstore_views
from flask import render_template
from flask import request, jsonify, make_response, abort




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
        if not email or not password:
            abort(400, 'Not a JSON')
        data = {
            'email': email,
            'password': password,
            'firstName': firstName,
            'lastName': lastName,
            'zipCode': zipCode,
            'street': street
        }
        user = User(**data)
        user.save()
        return make_response(jsonify(user.to_dict()), 201)
    
    return render_template('register.html')

