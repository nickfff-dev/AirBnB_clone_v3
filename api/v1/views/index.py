#!/usr/bin/python3
""" import Blueprint from flask """

from flask import jsonify
from api.v1.views import app_views
from flask import make_response
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return a successful status"""
    return make_response(jsonify({"status": "OK"}), 200)


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Return the number of each objects by type"""
    return make_response(jsonify({
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User')
    }), 200)
