#!/usr/bin/python3
""" Module for the api app """
from api.v1.views import app_views
from flask import Flask, render_template, make_response, jsonify

from flask_cors import CORS
from models import storage
from os import environ

app = Flask(__name__)

app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def close_storage(exception):
    """ Close the storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 404 page """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    """ Main Function """
    host = environ.get('ONBST_API_HOST', '0.0.0.0')
    port = environ.get('ONBST_API_PORT', '5008')
    app.run(host=host, port=port, threaded=True, debug=True)
