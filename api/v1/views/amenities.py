#!/usr/bin/python3
"""Amenity module"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity


r7 = "/amenities/<amenity_id>"


@app_views.route("/amenities", methods=["GET", "POST"], strict_slashes=False)
def all_amenities():
    """Get all amenities"""
    if request.method == "POST":
        body = request.get_json()
        if not body:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        if "name" not in body:
            return make_response(jsonify({"error": "Missing name"}), 400)
        new_amenity = Amenity(**body)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201
    all_amen = storage.all("State")
    amenities_all = []
    for k, v in all_amen.items():
        amenities_all.append(v.to_dict())
    return jsonify(amenities_all)


@app_views.route(r7, methods=["GET", "DELETE", "PUT"], strict_slashes=False)
def amenity(amenity_id):
    """single amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if request.method == 'PUT':
        body = request.get_json()
        if not body:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        for k, v in body.items():
            if k not in ['id', 'created_at', 'updated']:
                setattr(amenity, k, v)
                # body[k] = v
        storage.save()
        return jsonify(amenity.to_dict())
    if request.method == "DELETE":
        amenity.delete()
        storage.save()
        return jsonify({})
    return jsonify(amenity.to_dict())
