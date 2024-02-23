#!/usr/bin/python3
""" The flask application """
from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS
from web_dynamic.blue_prints import bookstore_views
from models import storage
from os import environ

app = Flask(__name__)
app.register_blueprint(bookstore_views)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.teardown_appcontext
def close_session(self):
    """ Closes the session """
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """ Handles 404 errors """
    return make_response(jsonify({'error': 'Not found'}), 404)



if __name__ == "__main__":
    host = environ.get('ONBST_API_HOST', '0.0.0.0')
    port = environ.get('ONBST_WEB_PORT', '5006')
    app.run(host=host, port=port, threaded=True, debug=True)