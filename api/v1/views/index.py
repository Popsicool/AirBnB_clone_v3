#!/usr/bin/python3
"""index module"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    """Return a Json Object 'status': 'OK'"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def stats():
    """stats"""
    all = {"amenities": "Amenity", "cities": "City", "places": "Place",
           "reviews": "Review", "states": "State", "users": "User"}
    all_stat = {}
    for k, v in all.items():
        all_stat[k] = storage.count(v)
    return jsonify(all_stat)
