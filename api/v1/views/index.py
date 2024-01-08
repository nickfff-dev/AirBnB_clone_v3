#!/usr/bin/python3
""" import Blueprint from flask """

from flask import jsonify
from api.v1.views import app_views
from flask import make_response


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return a successful status"""
    return make_response(jsonify({"status": "OK"}), 200)
